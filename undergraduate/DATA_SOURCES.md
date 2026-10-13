# Data sources

## Weather

Beijing, Shanghai, Singapore and Perth use **NSRDB Himawari PSM v3** data for **2019**, at **10-minute intervals**. The fields are global horizontal irradiance (GHI), direct normal irradiance (DNI), diffuse horizontal irradiance (DHI), air temperature and wind speed. Irradiance is expressed in W/m², temperature in °C and wind speed in m/s. Timestamps use local standard time.

Source: [NSRDB Himawari data and API documentation](https://developer.nlr.gov/docs/solar/nsrdb/himawari-download/). The selected weather-grid coordinates are recorded in `cities.json`.

Bangkok, Shenzhen, Seoul and Tokyo retain the weather and building files supplied with the original course material. The weather years are listed in the city table in `README.md`.

## Buildings

The four added cities use building footprints from **OpenStreetMap**, retrieved on **13 October 2026**. Each study area is approximately 2 km × 2 km. Footprints are selected by a representative point within the study boundary; building outlines and courtyard holes are retained. Modelled regional totals refer to these study areas.

© OpenStreetMap contributors. The added footprint datasets are distributed under the [Open Database License](https://opendatacommons.org/licenses/odbl/1-0/). See [OpenStreetMap copyright and attribution](https://www.openstreetmap.org/copyright). Study boundaries and building counts are recorded in `cities.json`.

## Cross-city analysis

Use consistent module parameters, mounting assumptions, roof fractions, analysis periods and units. Compare energy per module area or per roof area when studying resource differences across cities. Regional totals also depend on the building inventory and study area. Identify the denominator used for every normalized metric.
