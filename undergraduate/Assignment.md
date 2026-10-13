# BSE4610 Mini Project

Assess the solar resource and rooftop PV potential of a study area, then develop one extension that answers a question arising from your analysis. The mini-project contributes **20% of the final course grade** and is marked out of **100**.

## Core PV analysis

Select a city other than Bangkok or Shenzhen for the main analysis. The supplied assignment cities are Beijing, Shanghai, Singapore, Perth, Seoul and Tokyo.

Use `Solar_PV_Practical.ipynb` to calculate and visualize the following results. Select the figures required for your report.

| Task | Expected output | Marks |
|---|---|---:|
| City selection | Identify the study city and area. | 5 |
| Solar irradiance | Choose one visualization type from the options below. | 5 |
| Plane of array irradiance | Choose two visualization types; show fixed and tracking systems for each type. | 12 |
| POA comparison | Compare the mean daily POA profiles of fixed and tracking systems. | 3 |
| Module output | Calculate module DC power and compare the mean daily power profiles. | 5 |
| Building analysis | Show building footprints and rooftop PV potential. | 5 |
| Regional energy | Calculate the regional annual PV energy and plot building energy with building ID on the horizontal axis. | 5 |
| Energy per unit area | Report regional energy divided by total roof footprint area, in kWh/m². State the usable roof fraction. | 5 |
| Selected building | Show the selected building's tracking-system energy variation through the year. | 5 |
| **Core subtotal** | | **50** |

**Solar irradiance options:** a selected day; mean daily profile; monthly mean daily profiles; monthly means; or seasonal means.

**POA options:** a selected day; mean daily profile; monthly means; or seasonal means. Each selected type is worth 3 marks per configuration, giving 2 × 3 × 2 = 12 marks.

The Notebook reports both module-area yield and roof-area yield. Use the roof-area value for the assessed energy-per-unit-area task. Identify the area scenario used for regional totals and retain consistent assumptions when comparing systems.

## Extension

Choose **one** of the following directions. State your question, explain the analytical method, and support your conclusions with figures and numerical evidence.

### Cross-city comparison

Compare solar resources or PV potential across at least two cities. Keep metrics, analysis periods, system assumptions and units consistent. Quantify the differences and discuss likely drivers.

### Clustering

Group buildings, time periods or other relevant observations using selected features. Explain the feature selection and preprocessing, visualize the groups, and interpret the characteristics that distinguish them.

### Prediction

Predict a relevant solar or PV variable. Define the inputs and prediction target, train a suitable model, and evaluate it on data held out from fitting. For forecasting, preserve temporal order and use inputs available at the prediction time. Present predicted and observed values, quantify the errors, and discuss performance across conditions.

## Extension marking criteria

| Criterion | Assessment | Marks |
|---|---|---:|
| Visual clarity and aesthetics | Readable axes and legends, appropriate plot choices, consistent figures and a clear slide sequence. | 10 |
| Question and analytical design | A clear objective, a meaningful analytical setup, and justified data, variables and methods. | 10 |
| Technical implementation | Correct calculations or model implementation, a coherent workflow and reproducible results. | 10 |
| Depth and evidence of insights | Quantified findings, explanation of their significance and conclusions supported by results. | 15 |
| Critical reflection | Relevant limitations and plausible improvements or next steps. | 5 |
| **Extension subtotal** | | **50** |

## Submission

Submit executable code and a PowerPoint report with **up to 10 content slides, excluding the cover slide(s)**. State individual contributions on the cover. Include an AI-use declaration identifying the tools used and their role, or state that no AI tools were used.

Present the core assessment and extension in the same report. Label axes and units, provide informative captions, cite data sources, and state the principal modelling assumptions. Include the files needed to reproduce your results.

The final Notebook cell exports figures, data tables and calculation settings. Download your edited Notebook separately from Colab using **File > Download > Download .ipynb**.

[Full project guidelines and rubric](BSE4610_Mini_Project_Guidelines_and_Rubric.docx)
