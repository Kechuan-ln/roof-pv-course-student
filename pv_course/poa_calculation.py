"""Perez plane-of-array irradiance with explicit zero, night and missing-data rules."""
from functools import lru_cache
import numpy as np
import pandas as pd
import pvlib
import pytz
from timezonefinder import TimezoneFinder


@lru_cache(maxsize=16)
def get_timezone(latitude, longitude):
    name = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
    if name is None:
        raise ValueError('No timezone found for this location.')
    return pytz.timezone(name)


def _calculate(weather, latitude, longitude, tilt=None, azimuth=None):
    # Retain legacy timezone-localization behavior for the original notebooks.
    tz = get_timezone(latitude, longitude)
    if weather.index.tz is None:
        weather.index = weather.index.tz_localize(tz)
    else:
        weather.index = weather.index.tz_convert(tz)
    if weather.index.has_duplicates or not weather.index.is_monotonic_increasing:
        raise ValueError('Weather timestamps must be unique and ordered.')
    rad = weather[['GHI','DNI','DHI']]
    if (rad < 0).any().any():
        raise ValueError('Irradiance must be nonnegative.')
    solar = pvlib.solarposition.get_solarposition(weather.index, latitude, longitude)
    day = solar.apparent_zenith < 90
    tracking = tilt is None
    if tracking:
        tilt = solar.apparent_zenith.where(day, 0.)
        azimuth = solar.azimuth.where(day, 180.)
    elif not (np.isfinite(tilt) and 0 <= tilt <= 90 and np.isfinite(azimuth) and 0 <= azimuth <= 360):
        raise ValueError('Tilt must be 0–90° and azimuth 0–360°.')
    valid = np.isfinite(rad).all(axis=1)
    zeros = rad.eq(0).all(axis=1)
    active = valid & day & ~zeros
    components = pd.DataFrame(np.nan, index=weather.index,
                              columns=['poa_direct','poa_sky_diffuse','poa_ground'])
    components.loc[valid & (~day | zeros), :] = 0.
    if active.any():
        tilt_a = tilt.loc[active] if isinstance(tilt, pd.Series) else tilt
        az_a = azimuth.loc[active] if isinstance(azimuth, pd.Series) else azimuth
        s, r = solar.loc[active], rad.loc[active]
        total = pvlib.irradiance.get_total_irradiance(
            tilt_a, az_a, s.apparent_zenith, s.azimuth, r.DNI, r.GHI, r.DHI,
            dni_extra=pvlib.irradiance.get_extra_radiation(r.index), albedo=.2, model='perez')
        components.loc[active,'poa_direct'] = total['poa_direct']
        components.loc[active,'poa_sky_diffuse'] = total['poa_sky_diffuse']
        components.loc[active,'poa_ground'] = total['poa_ground_diffuse']
    result = {name:components[name] for name in components}
    result['total_poa'] = components.sum(axis=1, min_count=3)
    result.update(solar_zenith=solar.apparent_zenith, solar_azimuth=solar.azimuth)
    if tracking:
        result.update(surface_tilt=tilt, surface_azimuth=azimuth)
    return result


def calculate_poa(weather_data, surface_tilt, surface_azimuth, latitude, longitude):
    return _calculate(weather_data, latitude, longitude, surface_tilt, surface_azimuth)


def calculate_poa_track(weather_data, latitude, longitude):
    """Ideal dual-axis tracking during daylight, horizontal parked position at night."""
    return _calculate(weather_data, latitude, longitude)


def optimize_tilt_azimuth(weather_data, latitude, longitude, tilt_range=(0,90), azimuth_range=(90,270)):
    """5° grid maximum mean POA (W/m²), not continuous optimum or annual kWh/m²."""
    best = (0,180,-np.inf)
    for tilt in range(tilt_range[0], tilt_range[1]+1, 5):
        for azimuth in range(azimuth_range[0], azimuth_range[1]+1, 5):
            score = calculate_poa(weather_data,tilt,azimuth,latitude,longitude)['total_poa'].mean()
            if np.isfinite(score) and score > best[2]:
                best = (tilt,azimuth,float(score))
    if not np.isfinite(best[2]):
        raise ValueError('No valid irradiance available for optimization.')
    return best
