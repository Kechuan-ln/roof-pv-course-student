"""Roof geometry, module-area scaling and building energy statistics."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .data_quality import interval_energy, coverage_report


def energy_per_m2(pvout_data, module_area, step_minutes=10):
    """
    Convert module power output (W per module) into energy per square meter
    of module (Wh/m²) for each time step

    Parameters:
    -----------
    pvout_data : DataFrame or Series
        Power output of ONE PV module (W) with datetime index;
        a DataFrame must contain a 'power' column
    module_area : float
        Area of one PV module (m²)

    Returns:
    --------
    Series : Energy per m² of module for each time step (Wh/m²)
    """
    # Handle different input data formats
    if isinstance(pvout_data, pd.DataFrame):
        if 'power' not in pvout_data.columns:
            raise ValueError("pvout_data must contain a 'power' column")
        power = pvout_data['power']
    else:
        power = pvout_data

    if not np.isfinite(module_area) or module_area <= 0:
        raise ValueError('module_area must be positive.')
    return interval_energy(power, step_minutes) / module_area

def audit_buildings(buildings):
    """Remove exact footprint duplicates; report unresolved overlaps without merging."""
    if buildings.crs is None or buildings.empty:
        raise ValueError('Nonempty buildings with a CRS are required.')
    if buildings.geometry.isna().any() or buildings.geometry.is_empty.any() or not buildings.is_valid.all():
        raise ValueError('Missing, empty or invalid building geometry requires review.')
    if not buildings.geom_type.isin(['Polygon','MultiPolygon']).all():
        raise ValueError('Building footprints must be polygons.')
    import shapely
    keys = pd.Series(shapely.to_wkb(shapely.normalize(buildings.geometry.to_numpy())), index=buildings.index)
    duplicates = keys.duplicated()
    cleaned = buildings.loc[~duplicates].copy()
    if 'building_id' in cleaned and (cleaned.building_id.isna().any() or cleaned.building_id.duplicated().any()):
        raise ValueError('Building IDs must be unique and nonmissing.')
    crs = cleaned.crs
    local = cleaned if crs.utm_zone is not None else cleaned.to_crs(cleaned.estimate_utm_crs())
    summed = float(local.area.sum())
    union = float(shapely.union_all(local.geometry).area)
    report = dict(input_count=len(buildings), retained_count=len(cleaned),
                  exact_duplicates_removed=int(duplicates.sum()), sum_area_m2=summed,
                  union_area_m2=union, overlap_area_m2=max(0., summed-union),
                  overlap_fraction=max(0., (summed-union)/summed) if summed else 0.,
                  policy='Exact duplicates removed. Summed and union footprint areas are reported as separate geometric scenarios.')
    if 'type' in cleaned:
        report['types_for_review'] = cleaned['type'].value_counts().to_dict()
    return cleaned, report

def calculate_pv_potential(buildings, pvout_data, roof_efficiency=0.8, module_area=1.69, step_minutes=10):
    """
    Calculate the photovoltaic potential for each building

    Parameters:
    -----------
    buildings : GeoDataFrame
        GeoDataFrame containing building geometries
    pvout_data : DataFrame or Series
        Power output of ONE PV module (W) with datetime index
    roof_efficiency : float, default=0.8
        Efficiency factor for usable roof area (accounting for HVAC equipment, spacing, etc.)
    module_area : float, default=1.69
        Area of one PV module (m²), must match the value used in the PV output calculation

    Returns:
    --------
    buildings : GeoDataFrame
        Updated GeoDataFrame with PV potential calculations
    """
    if not np.isfinite(roof_efficiency) or not 0 < roof_efficiency <= 1:
        raise ValueError('roof_efficiency must be in (0,1].')
    buildings, geometry_report = audit_buildings(buildings)
    buildings.attrs['geometry_audit'] = geometry_report
    buildings.attrs['power_coverage'] = coverage_report(pvout_data.to_frame('power') if isinstance(pvout_data, pd.Series) else pvout_data, step_minutes)
    # Calculate the roof area (m²) in a local UTM projection.
    # Web Mercator (EPSG:3857) is only for map display: it inflates areas by 1/cos²(latitude)
    buildings['roof_area'] = buildings.to_crs(buildings.estimate_utm_crs()).geometry.area

    # Calculate usable area considering efficiency factor
    buildings['usable_area'] = buildings['roof_area'] * roof_efficiency

    # Energy yield per m² of PV module (Wh/m²)
    period_yield = energy_per_m2(pvout_data, module_area, step_minutes).sum(min_count=1)
    if pd.isna(period_yield):
        raise ValueError('No valid power observations: energy cannot be calculated.')

    # Calculate energy production in kWh for each building
    buildings['energy_kwh'] = buildings['usable_area'] * period_yield / 1000  # Convert from Wh to kWh

    return buildings

def create_statistics_plot(buildings):
    """
    Create statistical plots to analyze building PV potential
    
    Parameters:
    -----------
    buildings : GeoDataFrame
        GeoDataFrame containing building data with calculated PV potential
    """
    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histogram: Distribution of roof areas
    buildings['roof_area'].hist(ax=ax1, bins=50, color='skyblue', edgecolor='black')
    ax1.set_title('Distribution of Roof Areas')
    ax1.set_xlabel('Roof Area (m²)')
    ax1.set_ylabel('Number of Buildings')
    
    # Scatter plot: Roof area vs energy production
    ax2.scatter(buildings['roof_area'], buildings['energy_kwh'], 
               alpha=0.5, c='orange')
    ax2.set_title('Roof Area vs DC Energy')
    ax2.set_xlabel('Roof Area (m²)')
    ax2.set_ylabel('DC Energy (kWh)')
    
    plt.tight_layout()
