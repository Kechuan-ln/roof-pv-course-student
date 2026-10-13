# Rooftop PV Course

| Course | Colab entry | Scope |
|---|---|---|
| Undergraduate practical | [Open Notebook](https://colab.research.google.com/github/Kechuan-ln/roof-pv-course-student/blob/codex/colab-course/undergraduate/Solar_PV_Practical.ipynb) | Solar irradiance, fixed and tracking PV, module output and rooftop potential |
| PV assessment and coursework | [Open Notebook](https://colab.research.google.com/github/Kechuan-ln/roof-pv-course-student/blob/codex/colab-course/PV_Practical.ipynb) | Guided PV assessment, 3D shadows and independent clustering or forecasting investigation |

For the undergraduate practical, follow the [undergraduate instructions](undergraduate/README.md). The instructions below cover PV assessment and coursework.

Complete the guided practical for Part A, then develop a clustering or forecasting investigation for Part B. Present both in one coursework report. Keep the complete package together in a writable local folder.

## 1. Start in Google Colab

[Open the practical in Colab](https://colab.research.google.com/github/Kechuan-ln/roof-pv-course-student/blob/codex/colab-course/PV_Practical.ipynb)

1. Sign in to Google and choose **File > Save a copy in Drive** so you can edit and save your own work.
2. Use a **CPU** runtime. Run the first code cell under **Prepare the Course**. It downloads the course code and all four cities, installs libraries and checks the data.
3. Continue from top to bottom with **Shift + Enter**, or choose **Runtime > Run all**. If setup asks for a session restart after updating a loaded library, restart and rerun from the first cell.
4. Save your Notebook regularly. The final cell downloads `PV_Results.zip`, containing the website and calculation results. Extract it and open `result/course_website.html` in your browser.
5. Download your edited Notebook separately with **File > Download > Download .ipynb** when submitting your work.

The setup cell selects a fixed course release. Each new Colab runtime needs setup again. Your saved Notebook is kept in Drive; files created inside the runtime must be downloaded before that runtime ends.

### Local alternative on Windows or macOS

1. Extract the complete student ZIP to a writable folder.
2. Install Anaconda or Miniconda once.
3. On Windows, double-click `Start_Course.bat`. On macOS, double-click `Start_Course.command`; if necessary, right-click and choose Open for the first launch.
4. Keep the launch window open. It prepares Python 3.12, checks the environment and opens the same `PV_Practical.ipynb` in JupyterLab.
5. Run cells from top to bottom. The final cell provides a results ZIP link. Save the Notebook with **Ctrl + S** (Windows) or **Command + S** (macOS).

If you already have local Jupyter with Python 3.12, open the Notebook from the extracted student folder and run the environment cell first. Colab uses `requirements-colab.txt`; local launchers use `requirements.txt` and `mini_project.yml`.

## 2. Guided practical: Explore and assess a roof

Open `PV_Practical.ipynb`.

- Choose one of the supplied cities: Bangkok, Shenzhen, Seoul, or Tokyo.
- Explore weather, solar radiation, building heights, and 3D shadows.
- Compare fixed mounting with ideal dual-axis tracking.
- Investigate tilt and estimate a building's rooftop electricity generation.
- Record your observations and design recommendation in the Notebook.

Change the parameters in the indicated cells. After changing an upstream setting, rerun the dependent cells in order.

The last website-export cell creates `result/course_website.html`. Colab displays an embedded preview; local Jupyter displays a file link. You can open the exported HTML offline after downloading the results ZIP. It shows **Buildings and Energy** and **Sun and Shadows**. Run the shadow cell before exporting if you want the 3D scene included. After recalculating, rerun the export cell to update the website.

## 3. Coursework investigation

Read `Assignment.md`. Choose **short-term PV forecasting** or **weather-type clustering**, using one of the four included cities.

[Assignment.md](Assignment.md) sets out the tasks and marks: PV assessment **30 marks**, clustering or forecasting **50 marks**, and conclusions and communication **20 marks**. Include both the practical assessment and your investigation in one report. For Part B in Colab, save a second copy of the practical as `My_Investigation.ipynb`, keep its Prepare the Course section and first code cell, and replace the remaining cells with your own analysis. Run setup in that Notebook to download its data. In local Jupyter, create `My_Investigation.ipynb` beside the practical and use the same course environment.

### Included assignment data

The Colab setup downloads all four cities with training, validation and test data. The local student ZIP includes the same files. Bangkok has this structure:

```text
assignment_data/
└── Bangkok/
    ├── train/
    │   ├── observations.csv
    │   ├── samples.csv
    │   ├── targets.csv
    │   └── submission_template.csv
    ├── validation/
    │   └── ...
    └── test/
        └── ...
```

Keep the filenames and folders supplied by the instructor. Use the matching city folder in your data-loading code. For example, read `assignment_data/Bangkok/train/observations.csv` for Bangkok training observations.

| File or split | Purpose |
|---|---|
| `observations.csv` | Time-stamped weather and simulated module power; suitable for forecasting or weather clustering |
| `samples.csv` | Forecast sample IDs, issue times, and target times one hour later |
| `targets.csv` | Target power for each sample ID |
| `submission_template.csv` | Forecast result format: `sample_id,prediction_W` |
| `train/` | Fit preprocessing and models |
| `validation/` | Compare approaches and choose settings |
| `test/` | Evaluate the final approach after selecting settings on validation data |

Use the field guide in `assignment_data/README.md`. Preserve chronological order for forecasting. Input features must use information available at or before the issue time. Fit scaling and other learned preprocessing on the training data. Preserve missing intervals when constructing history windows.

### Investigate and report

- **Forecasting:** predict simulated single-module DC power one hour ahead. Compare persistence with a lightweight model, report MAE and RMSE, and show prediction-versus-target curves for specific dates.
- **Clustering:** select a time scale and weather features, explain scaling and the choice of cluster count, and interpret the groups through their solar-resource characteristics.
- For either task, use the first experiment to identify a question or weakness, then design a second experiment to investigate it.

Your instructor may show a separate interactive demonstration. The assignment remains your own implementation and investigation.

The detailed five-level grading matrix is in [Assessment_Rubric.docx](Assessment_Rubric.docx).

## 4. Submit your work

Submit Parts A and B together:

1. Your completed practical Notebook and your investigation Notebook, including outputs and explanations.
2. One PDF or PowerPoint report of **no more than 10 pages/slides in total**, including the cover, individual contributions and references. Cover the question, practical assessment, investigation, comparisons and conclusions.
3. Your result files and generated practical website. Forecast outputs use `sample_id,prediction_W`; clustering outputs identify the time periods and features associated with each label.

State that power values are simulated module DC output and explain how you used AI tools. Select settings on validation data before evaluating the test split. Follow the instructor's submission instructions. Keep practical calculations and observations in `PV_Practical.ipynb`.

## 5. What is in this package?

| Item | How you use it |
|---|---|
| `PV_Practical.ipynb` | Guided practical calculations, visualizations, and your observations |
| `Assignment.md` | Coursework tasks, marks and submission checklist |
| `Assessment_Rubric.docx`, `Assessment_Rubric.pdf` | Detailed grading criteria |
| `assignment_data/` | Included data for four cities, with train/validation/test splits |
| `weather_data/`, `buildings_data/` | Included practical input data |
| `result/` | Generated results and the practical website |
| `course_website.py` | Website export entry point, called by the Notebook |
| `pv_course/`, `course_assets/` | Supporting functions and website templates; keep these with the package |
| `scripts/`, `requirements-colab.txt` | Colab setup and checks |
| `Start_Course.*`, `mini_project.yml`, `requirements.txt` | Local environment and launch support |

## 6. If something does not run

- **Assignment data are missing:** in Colab, rerun the first setup cell in the active Notebook. Locally, check that you extracted the complete student package.
- **A variable is undefined:** restart the kernel and run the cells in order from the top.
- **Imports fail:** run the setup cell first. Follow any session-restart instruction. For local Python version errors, use `Start_Course`.
- **Installation fails:** retain the error message and retry when the connection is available.
- **The website shows old results:** rerun the relevant calculation and export cells, then refresh the page.
- **The 3D view is missing after reopening:** rerun the shadow cell and export the website again.

If the issue persists, send your instructor the error message, the cell that produced it, and your operating system.

### Local environment check

In the course environment, run `python scripts/check_environment.py requirements.txt`, then `python scripts/smoke_check.py`. The second command checks scientific imports, geometry file I/O, solar position, shadow calculations, plotting, and small clustering/prediction models. First-time imports may take longer. If a check fails, retain its output for your instructor.
