# Assignment Data

Bangkok, Shenzhen, Seoul and Tokyo are included. Each city contains `train/` (January–August), `validation/` (September–October) and `test/` (November–December), plus `source_metadata.json`. After running the Colab setup cell, or from a local Notebook beside `PV_Practical.ipynb`, read `assignment_data/Bangkok/train/observations.csv`. All splits include observations, forecast samples, targets and a submission template.

## Observation fields

| Field | Meaning | Unit |
|---|---|---|
| timestamp | Local observation time with UTC offset | ISO timestamp |
| power | Simulated single-module DC power | W |
| GHI | Global horizontal irradiance | W/m² |
| DNI | Direct normal irradiance | W/m² |
| DHI | Diffuse horizontal irradiance | W/m² |
| Temperature | Air temperature | °C |
| Wind Speed | Wind speed | m/s |
| solar_zenith | Angle between the Sun and the vertical | degrees |

Records are spaced 10 minutes apart where data are present. Shenzhen uses 2020 and omits February 29; the other supplied cities use 2019. Preserve missing intervals when forming history windows.

## Forecast sample files

`samples.csv` contains sample_id, issue_time, and target_time. The target is power at one instant one hour after the issue time. Use only observations available at or before issue_time to build features.

`targets.csv` maps sample_id to target_power_W. Join by sample_id. `submission_template.csv` contains sample_id and the prediction_W column for your results.

For weather clustering, aggregate `observations.csv` to your chosen time scale, such as one day. Explain your feature construction and preprocessing.

Test labels are included for final evaluation after selecting settings on validation data. See [the student README](../README.md) and [Assignment.md](../Assignment.md) for the task and submission requirements.
