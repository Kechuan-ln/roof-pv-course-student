# Regional Solar Energy Potential Analysis

An undergraduate practical in solar energy assessment. The sequence is solar irradiance, fixed and tracking POA, module DC output, and rooftop PV potential.

[Open in Google Colab](https://colab.research.google.com/github/Kechuan-ln/roof-pv-course-student/blob/codex/colab-course/undergraduate/Solar_PV_Practical.ipynb)

1. Save a copy in Drive and use a CPU runtime.
2. Run the first cell to download the code and four-city data and install dependencies.
3. Run the remaining cells in order. Change `CITY` to Bangkok, Shenzhen, Seoul or Tokyo.
4. Use `DAY`, `SURFACE_TILT`, `ROOF_FRACTION` and `BUILDING_ID` for comparisons. Rerun dependent cells after changes.
5. Run the final cell to download figures, CSV tables and calculation settings. Download the edited Notebook separately from the File menu.

The Notebook has 10 code cells. Mean irradiance is expressed in W/m²; integrated irradiation in kWh/m²; simulated module power in W; and energy in kWh.

## Mini-project

Select a city other than Bangkok or Shenzhen for the main analysis. The supplied assignment cities are Seoul and Tokyo. Read [Assignment.md](Assignment.md) for the tasks, submission requirements and marking criteria. The project contributes 20% of the final course grade: core PV analysis earns 50 marks and one extension earns 50 marks. Choose cross-city comparison, clustering or prediction for the extension.

Submit executable code and a PowerPoint report with up to 10 content slides, excluding the cover. State individual contributions on the cover, include an AI-use declaration, and cite data sources and modelling assumptions.

The detailed assessment document is [Mini-project guidelines and rubric](BSE4610_Mini_Project_Guidelines_and_Rubric.docx).

## Local Jupyter

Extract the complete package, open `Solar_PV_Practical.ipynb` from its folder in a Python 3.12 Jupyter environment, and run the first cell. It installs the same requirements. Colab is the default entry for students who do not have a local Python environment.

## Files

- `Solar_PV_Practical.ipynb`: classroom calculations and figures.
- `weather_data/`, `buildings_data/`: original four-city input data.
- `pv_course/`, `scripts/`, `requirements.txt`: supporting functions and setup.
- `result/`: generated figures and tables.

After the initial setup, the calculations and maps use downloaded files. The footprint maps use projected coordinates and require no map-tile service.
