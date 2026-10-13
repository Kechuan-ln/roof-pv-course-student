"""One reproducible physical assessment and timestamped forecasting export."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from .weather_visualization import read_weather
from .poa_calculation import calculate_poa, calculate_poa_track, get_timezone
from .Efficiency_calculation import calculate_pv_efficiency
from .building_pv_potential import calculate_pv_potential
from .data_quality import coverage_report, interval_energy

CITIES = ('Bangkok','Shenzhen','Seoul','Tokyo')
MODULE_PARAMETERS = dict(gamma_ref=1.,mu_gamma=.002,I_L_ref=7.3,I_o_ref=1e-10,
    R_sh_ref=400.,R_s=.3,R_sh_0=3000.,cells_in_series=60,alpha_sc=.004,
    EgRef=1.12,irrad_ref=1000.,temp_ref=25.)


def run_assessment(city='Bangkok', root=None, output_dir=None, module_area=1.69,
                   roof_fraction=.8, surface_tilt=None, surface_azimuth=180., step_minutes=10):
    if city not in CITIES:
        raise ValueError(f'city must be one of {CITIES}')
    root=Path(root or Path(__file__).resolve().parents[1])
    output=Path(output_dir or root/'result'/'assessment'/city)
    weather_path=root/'weather_data'/f'{city}_weather.csv'
    buildings_path=root/'buildings_data'/f'{city}_building.geojson'
    weather=read_weather(weather_path)
    buildings=gpd.read_file(buildings_path)
    centroids=buildings.to_crs(buildings.estimate_utm_crs()).centroid.to_crs(4326)
    latitude,longitude=float(centroids.y.mean()),float(centroids.x.mean())
    weather.index=weather.index.tz_localize(get_timezone(latitude,longitude))
    weather.index.name='timestamp'
    tilt=abs(latitude) if surface_tilt is None else surface_tilt
    fixed=pd.DataFrame(calculate_poa(weather,tilt,surface_azimuth,latitude,longitude))
    tracking=pd.DataFrame(calculate_poa_track(weather,latitude,longitude))
    power_fixed=calculate_pv_efficiency(fixed,weather,MODULE_PARAMETERS,module_area)
    power_tracking=calculate_pv_efficiency(tracking,weather,MODULE_PARAMETERS,module_area)
    roofs=calculate_pv_potential(buildings,power_fixed,roof_fraction,module_area,step_minutes)
    audit=roofs.attrs['geometry_audit']
    weather_coverage=coverage_report(weather,step_minutes)
    power_coverage=coverage_report(power_fixed[['power']],step_minutes)
    rows={}
    for name,poa,power in [('fixed',fixed,power_fixed),('tracking',tracking,power_tracking)]:
        module_kwh=float(interval_energy(power.power,step_minutes).sum(min_count=1)/1000)
        rows[name]=dict(poa_kwh_m2=float(interval_energy(poa.total_poa,step_minutes).sum(min_count=1)/1000),
            module_kwh=module_kwh,module_kwh_m2=module_kwh/module_area,
            summed_footprint_scenario_mwh=audit['sum_area_m2']*roof_fraction*module_kwh/module_area/1000,
            union_footprint_scenario_mwh=audit['union_area_m2']*roof_fraction*module_kwh/module_area/1000)
    summary=pd.DataFrame.from_dict(rows,orient='index')
    output.mkdir(parents=True,exist_ok=True)
    forecast=weather[['GHI','DNI','DHI','Temperature','Wind Speed']].copy()
    forecast.insert(0,'power',power_fixed.power)
    forecast['solar_zenith']=fixed.solar_zenith
    csv_path=output/'forecast_input.csv'
    forecast.to_csv(csv_path,index_label='timestamp')
    metadata=dict(city=city,timezone=str(weather.index.tz),latitude=latitude,longitude=longitude,
        step_minutes=step_minutes,module_area_m2=module_area,roof_fraction=roof_fraction,
        surface_tilt=float(tilt),surface_azimuth=float(surface_azimuth),module_parameters=MODULE_PARAMETERS,
        target_kind='simulated_module_dc_power',power_unit='W',irradiance_unit='W/m²',
        interval_convention='Each record treated as interval-mean value over step_minutes; verify source convention before field use.',
        year_convention='Energy over supplied records; no leap-day imputation or annual extrapolation.',
        omitted_losses=['incidence-angle','soiling','wiring','inverter','building/row shading'],
        weather_coverage=weather_coverage,power_coverage=power_coverage,geometry_audit=audit,
        source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [weather_path,buildings_path]},
        csv_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest())
    csv_path.with_suffix('.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    summary.to_csv(output/'assessment_summary.csv',index_label='system')
    fixed.to_csv(output/'poa_fixed.csv',index_label='timestamp')
    tracking.to_csv(output/'poa_tracking.csv',index_label='timestamp')
    power_fixed.drop(columns='timestamp').to_csv(output/'power_fixed.csv',index_label='timestamp')
    power_tracking.drop(columns='timestamp').to_csv(output/'power_tracking.csv',index_label='timestamp')
    roofs.drop(columns='geometry').to_csv(output/'building_energy.csv',index=False)
    return dict(weather=weather,buildings=roofs,poa_fixed=fixed,poa_tracking=tracking,
        power_fixed=power_fixed,power_tracking=power_tracking,summary=summary,
        geometry_audit=audit,metadata=metadata,forecast_csv=csv_path,output_dir=output)
