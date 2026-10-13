# Coursework: Assess Rooftop PV and Investigate Its Data

Submit one report combining **A. PV assessment (30 marks)**, **B. clustering or forecasting (50 marks)** and **C. conclusions and communication (20 marks)**. Total: **100 marks**.

## Getting started

1. Choose Bangkok, Shenzhen, Seoul, or Tokyo. Use the same city for Parts A and B unless your question requires a comparison.
2. Open `PV_Practical.ipynb` in Colab, save a copy in Drive, run its setup cell and retain your calculations, figures and observations for Part A.
3. Read `assignment_data/README.md`. All four cities include train, validation and test data, labels and forecast submission templates.
4. For Part B in Colab, save a second copy as `My_Investigation.ipynb`. Keep the Prepare the Course section and first code cell, and replace the remaining cells with your own analysis. Run setup in that Notebook. Locally, create `My_Investigation.ipynb` beside the practical and use the course environment.

## A. PV resource and rooftop assessment — 30 marks

Use the supplied practical functions. Select representative figures for the report and keep the full calculations in your Notebook.

| Criterion | Marks | Required evidence |
|---|---:|---|
| City and solar resource | 6 | Identify the city and data period; use daily, monthly or seasonal plots to explain a resource pattern. |
| Fixed versus tracking systems | 8 | Compare POA irradiance and electricity generation; quantify tracking gain and discuss its implications. |
| Rooftop PV potential | 10 | Show the building map, regional energy total, energy per unit module area, and results for one selected building. State units and assumptions, including usable roof fraction. |
| Parameters and shadows | 6 | Change tilt or usable roof fraction and compare results; show shadows at two times and explain the difference. |

For each criterion, half the marks reward correct calculations and readable figures; half reward quantitative interpretation and a supported judgment. Report the footprint overlap information and explain its effect on the regional estimate. The shadow scene illustrates geometric shading; the energy estimates use the unshaded module model.

## B. Independent investigation — 50 marks

Choose **one** track. State a specific question, expected result, controlled variables and evaluation method. Present an initial experiment, identify an error or pattern, then conduct a second experiment to test an explanation.

| Criterion | Marks | Forecasting evidence | Clustering evidence |
|---|---:|---|---|
| Question and data preparation | 10 | Define history, one-hour forecast horizon, chronological splits and missing-data handling. | Define the time scale, weather features, missing-data handling and scaling. |
| Initial implementation | 10 | Implement persistence (latest observed power) and one lightweight model. | Implement clustering and show groups and representative weather profiles. |
| Controlled comparison | 10 | Compare methods, history lengths or feature sets on common evaluation samples. | Compare feature sets, scaling choices or cluster counts on the same periods. |
| Analysis of results | 10 | Report MAE and RMSE, prediction-versus-target curves and a difficult period. | Explain group sizes, feature differences, representative periods and ambiguous cases; justify a quality measure. |
| Evidence-led second experiment | 10 | Use an observed error to motivate a change, test it and explain the outcome. | Use a grouping weakness to motivate a change, test it and explain the outcome. |

The comparison row rewards a fair experimental setup and numerical comparison. The second-experiment row rewards the link between the initial evidence, your hypothesis, the change and its interpretation. A well-designed experiment can earn full marks even when performance does not improve. Method complexity earns no additional marks.

### Data and evaluation

For forecasting, use observations available at or before each issue time to predict simulated single-module DC power at one instant one hour later. Fit preprocessing and models on training data; select settings using validation data; evaluate the selected approach once on test data. Test labels are included for this final evaluation. State which target times are included in the evaluation and use identical samples for model comparisons. Report how many samples you excluded because of missing history.

For clustering, use training periods to develop features, scaling and groups; use validation periods to compare settings. Inspect the selected method on test periods to discuss whether patterns persist across seasons. Explain how new periods receive a group label. Solar-resource profiles and interpretation should accompany any numerical clustering score.

## C. Conclusions and communication — 20 marks

| Criterion | Marks | Required evidence |
|---|---:|---|
| Integrated conclusions and recommendations | 10 | Use numerical evidence from Parts A and B to support a PV-related conclusion or recommendation; identify an assumption or uncertainty that could change it. |
| Report quality | 5 | Organize the report around your question. Give plots readable labels, units, legends and captions. |
| Reproducibility and contributions | 5 | Provide runnable Notebooks, settings and result files. State individual contributions and how AI tools were used. |

## How work is graded

See [Assessment_Rubric.docx](Assessment_Rubric.docx) for criterion-specific descriptions at five levels: F (Inadequate), D (Barely adequate), C (Satisfactory), B (Good) and A (Outstanding). The criterion marks match the tables above. The assessor records marks and supporting evidence for each criterion; institutional rules govern grade conversion.

## Submit your work

- Your completed `PV_Practical.ipynb` and `My_Investigation.ipynb`, including outputs and explanations.
- **One report of no more than 10 pages/slides in total**, including the cover, contributions and references. Submit a PDF or PowerPoint. Suggested allocation: cover and question 1 page, Part A 3 pages, Part B 4 pages, conclusions 1 page, contributions and references 1 page.
- Relevant result files and the generated `result/course_website.html` from Part A.
- For forecasting, a CSV with `sample_id,prediction_W` for evaluated test samples, with exclusions documented. For clustering, a table identifying each evaluated period, its features and cluster label.

State that power values are simulated module DC output. Follow your instructor's submission location and deadline.
