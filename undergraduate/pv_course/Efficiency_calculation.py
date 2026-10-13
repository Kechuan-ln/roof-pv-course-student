"""Vectorized simulated module DC power. Missing observations remain missing."""
import numpy as np
import pandas as pd
import pvlib
from .data_quality import validate_time_index


def calculate_pv_efficiency(poa_data, weather_data, module_parameters, module_area):
    if not np.isfinite(module_area) or module_area <= 0:
        raise ValueError('module_area must be a positive area in m².')
    validate_time_index(poa_data.index)
    if not poa_data.index.equals(weather_data.index):
        raise ValueError('POA and weather must have identical timestamps and timezone.')
    irr = pd.DataFrame({'poa':poa_data['total_poa'],
                        'temperature':weather_data['Temperature'],
                        'wind':weather_data['Wind Speed']})
    if (irr[['poa','wind']] < 0).any().any():
        raise ValueError('Irradiance and wind must be nonnegative.')
    valid = np.isfinite(irr).all(axis=1)
    out = pd.DataFrame(np.nan, index=irr.index, columns=['efficiency','power'])
    zero = valid & irr.poa.eq(0)
    out.loc[zero, ['efficiency','power']] = 0.
    active = valid & irr.poa.gt(0)
    if active.any():
        data = irr.loc[active]
        cell_temp = pvlib.temperature.sapm_cell(data.poa, data.temperature, data.wind,
            **pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_polymer'])
        params = pvlib.pvsystem.calcparams_pvsyst(data.poa, cell_temp, **module_parameters)
        power = pvlib.pvsystem.singlediode(*params, method='lambertw')['p_mp']
        if not np.isfinite(power).all() or (power < 0).any():
            raise ValueError('The module model produced invalid power for finite inputs.')
        out.loc[active,'power'] = power
        out.loc[active,'efficiency'] = power / data.poa / module_area
    out['timestamp'] = out.index
    return out
