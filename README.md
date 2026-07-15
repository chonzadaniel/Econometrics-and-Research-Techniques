# Difference-in-Differences Minimum Wage Analysis Using Python

## Project Overview

This project applies the **Difference-in-Differences (DiD)** econometric method to estimate the impact of the April 1992 New Jersey minimum wage increase on fast-food restaurant employment.

The analysis compares changes in **full-time equivalent employment (FTE)** between:

- **New Jersey**, the treatment group affected by the minimum wage increase
- **Pennsylvania**, the comparison group not affected by the same policy change

The project demonstrates how Python can be used for applied econometrics, causal inference, policy analysis, and evidence-based decision-making.

---

## Research Question

Did the April 1992 minimum wage increase in New Jersey reduce fast-food restaurant employment relative to Pennsylvania?

---

## Problem Statement

Minimum wage policy remains one of the most debated topics in labour economics and public policy. A common concern is that increasing the minimum wage may increase labour costs and force employers to reduce employment. However, the real-world employment effect of minimum wage changes depends on several factors, including labour demand, market conditions, pricing responses, worker productivity, employee turnover, and firm-level adjustment strategies.

In April 1992, New Jersey increased its minimum wage, while neighbouring Pennsylvania did not experience the same policy change. This setting provides an opportunity to estimate the employment effect of the policy by comparing employment changes in New Jersey restaurants with employment changes in Pennsylvania restaurants before and after the intervention.

This project uses a Difference-in-Differences framework to assess whether employment in New Jersey changed differently after the minimum wage increase compared with Pennsylvania.

---

## Objective

The main objective of this project is to estimate the impact of the April 1992 New Jersey minimum wage increase on fast-food restaurant employment using a Difference-in-Differences linear regression framework.

Specific objectives are to:

1. Load and prepare the minimum wage dataset for econometric modeling.
2. Define the treatment group, comparison group, pre-policy period, and post-policy period.
3. Construct the Difference-in-Differences interaction term.
4. Estimate a baseline Difference-in-Differences model.
5. Estimate a full linear regression model with restaurant-level control variables.
6. Apply p-value based model refinement while preserving the core DiD variables.
7. Estimate the final selected model.
8. Visualize the observed and counterfactual employment paths.
9. Interpret the policy and business meaning of the estimated treatment effect.

---

## Methodological Approach

The project uses a **Difference-in-Differences** framework.

The baseline model is:

$$
FTE_i = \beta_0 + \beta_1 NJ_i + \beta_2 POST_i + \beta_3(NJ_i \times POST_i) + \varepsilon_i
$$

where:

| Symbol | Meaning |
|---|---|
| FTEᵢ | Full-time equivalent employment for restaurant i |
| NJᵢ | Treatment indicator: 1 if the restaurant is in New Jersey, 0 if in Pennsylvania |
| POSTᵢ | Post-policy indicator: 1 after April 1992, 0 before April 1992 |
| NJᵢ × POSTᵢ | Difference-in-Differences interaction term |
| β₀ | Baseline employment level for Pennsylvania before the policy |
| β₁ | Baseline difference between New Jersey and Pennsylvania |
| β₂ | Employment change in Pennsylvania after April 1992 |
| β₃ | Difference-in-Differences treatment effect |
| εᵢ | Error term |

The coefficient of interest is:

$$
\beta_3
$$

This coefficient estimates whether employment in New Jersey changed differently after the minimum wage increase compared with Pennsylvania.

---

## Dataset

The project uses the dataset:

```text
njmin3.csv
```

The dataset contains restaurant-level information for fast-food establishments in New Jersey and Pennsylvania before and after the April 1992 minimum wage change.

### Key Variables

| Variable | Description |
|---|---|
| `fte` | Full-time equivalent employment |
| `NJ` | Treatment indicator: 1 = New Jersey, 0 = Pennsylvania |
| `POST_APRIL92` | Post-policy indicator: 1 = after April 1992, 0 = before April 1992 |
| `NJ_POST_APRIL92` | Interaction term: `NJ × POST_APRIL92` |
| `bk` | Burger King restaurant indicator |
| `kfc` | KFC restaurant indicator |
| `roys` | Roy Rogers restaurant indicator |
| `wendys` | Wendy’s restaurant indicator |
| `co_owned` | Company-owned restaurant indicator |
| `centralj` | Central New Jersey region indicator |
| `southj` | South New Jersey region indicator |
| `pa1` | Pennsylvania region indicator 1 |
| `pa2` | Pennsylvania region indicator 2 |

---

## Project Structure

Recommended project structure:

```text
Econometrics-and-Research-Techniques/
│
├── Difference-in-Difference-MinimumWage.py
├── njmin3.csv
├── requirements.txt
├── README.md
│
└── outputs/
```

The Python script is designed to check for the dataset in either:

```text
./njmin3.csv
```

or:

```text
./data/njmin3.csv
```

---

## End-to-End Workflow

The Python script performs the following steps:

1. Imports required Python libraries.
2. Loads the `njmin3.csv` dataset.
3. Checks basic data quality issues.
4. Removes duplicate rows if they exist.
5. Drops observations with missing `fte` values.
6. Recreates the DiD interaction term.
7. Defines the outcome, treatment, post-policy, and interaction variables.
8. Runs the baseline Difference-in-Differences model.
9. Runs a full model with restaurant chain, ownership, and regional controls.
10. Applies backward p-value based feature selection.
11. Preserves the core DiD variables throughout model refinement.
12. Fits the final selected model.
13. Extracts the final DiD estimate.
14. Computes observed and counterfactual employment values.
15. Plots the DiD impact visualization.
16. Prints a final policy interpretation.

---

## Statistical Modeling Strategy

### Baseline DiD Model

```text
fte ~ NJ + POST_APRIL92 + NJ_POST_APRIL92
```

This model estimates the basic Difference-in-Differences effect without additional controls.

### Full Controlled Model

```text
fte ~ NJ + POST_APRIL92 + NJ_POST_APRIL92 + controls
```

Additional controls may include restaurant chain, ownership status, and regional indicators.

### Final Selected Model

The final model is obtained through backward p-value based feature selection. Insignificant control variables are removed step by step, while the core Difference-in-Differences variables are retained throughout the process.

The following variables are protected and are never removed:

```text
NJ
POST_APRIL92
NJ_POST_APRIL92
```

These variables define the Difference-in-Differences design.

---

## Modeling Results Summary

The modeling workflow estimates three main stages:

1. **Baseline Difference-in-Differences model**
   - Uses only `NJ`, `POST_APRIL92`, and `NJ_POST_APRIL92`.
   - Provides the core DiD treatment-effect estimate.

2. **Full controlled linear regression model**
   - Adds restaurant chain, ownership, and regional controls.
   - Tests whether observable restaurant characteristics affect employment levels.

3. **Final selected model**
   - Removes statistically insignificant control variables.
   - Preserves the core DiD structure.
   - Produces the final treatment-effect estimate.

The key coefficient is:

```text
NJ_POST_APRIL92
```

This coefficient represents the estimated policy impact of the New Jersey minimum wage increase.

---

## Final Results

The final Difference-in-Differences estimate is approximately:

```text
+2.68 FTE employees
```

This means that, after the April 1992 minimum wage increase, New Jersey fast-food restaurants had approximately **2.68 more full-time equivalent employees** relative to the Pennsylvania counterfactual trend.

The result does **not** support the claim that the New Jersey minimum wage increase reduced fast-food employment.

Instead, the estimated effect suggests that employment in New Jersey increased relative to what would have been expected if New Jersey had followed the Pennsylvania trend.

---

## Final Visualization

The final Difference-in-Differences visualization shows:

- Observed Pennsylvania employment trend
- Observed New Jersey employment trend
- Counterfactual New Jersey employment trend
- Estimated DiD treatment-effect gap

The most important visual feature is the vertical gap between:

```text
Observed post-policy New Jersey employment
```

and:

```text
Counterfactual post-policy New Jersey employment
```

That gap represents the estimated Difference-in-Differences treatment effect.

The visualization supports the regression result that the minimum wage increase was not associated with a relative employment decline in New Jersey.

---

## Business and Policy Recommendations

### 1. Avoid assuming that minimum wage increases automatically reduce employment

The results do not support the assumption that the April 1992 New Jersey minimum wage increase reduced fast-food employment. Policy discussions should therefore avoid automatic conclusions that higher minimum wages necessarily lead to job losses.

### 2. Use evidence-based policy evaluation

Labour-market policies should be evaluated using empirical evidence. Difference-in-Differences provides a structured method for comparing affected and unaffected groups before and after policy changes.

### 3. Consider business adjustment mechanisms

The absence of a negative employment effect suggests that restaurants may adjust to higher wages through mechanisms other than reducing employment. These may include:

- Small price increases
- Improved worker productivity
- Reduced employee turnover
- Better scheduling
- Absorbing costs through margins
- Operational restructuring
- Increased consumer demand

### 4. Strengthen future analysis with more data

Future evaluations could be improved by including:

- More pre-policy periods
- More post-policy periods
- Store-level fixed effects
- Time fixed effects
- Wage data
- Price data
- Revenue and profit indicators
- Employee turnover measures
- Alternative comparison states
- Sensitivity checks

### 5. Interpret findings within the DiD assumptions

The Difference-in-Differences estimate depends on the **parallel trends assumption**. This means that, without the policy intervention, employment in New Jersey would have followed a similar trend to Pennsylvania.

The results should therefore be interpreted within the credibility of this assumption.

---

## Causal Inference Assumption

The Difference-in-Differences method depends on the **parallel trends assumption**.

This means that, in the absence of the minimum wage increase, employment trends in New Jersey would have followed a similar pattern to employment trends in Pennsylvania.

The credibility of the DiD estimate depends on whether Pennsylvania provides a reasonable comparison group for New Jersey.

---

## Limitations

This project is designed for applied econometric learning and policy-impact demonstration. Key limitations include:

- The parallel trends assumption is not directly proven in the script.
- Results depend on model specification and selected controls.
- The analysis uses observational data rather than randomized experimental data.
- P-value based feature selection should be interpreted carefully.
- Statistical significance should be considered alongside economic and policy relevance.
- The DiD estimate reflects association under the research design assumptions and should not be interpreted as automatic proof of causality without those assumptions.

---

## Installation and Environment Setup

### Create a virtual environment

```bash
python3.11 -m venv .venv
```

### Activate the virtual environment

For macOS or Linux:

```bash
source .venv/bin/activate
```

### Install required packages

```bash
pip install pandas numpy matplotlib seaborn statsmodels
```

Alternatively, install packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Suggested `requirements.txt`

```text
numpy
pandas
matplotlib
seaborn
statsmodels
```

---

## How to Run the Project

From the project root folder, run:

```bash
python Difference-in-Difference-MinimumWage.py
```

Make sure `njmin3.csv` is available either in the project root or inside a `data/` folder.

---

## Example Terminal Workflow

```bash
cd Econometrics-and-Research-Techniques
source .venv/bin/activate
python Difference-in-Difference-MinimumWage.py
```

---

## Expected Outputs

The script prints:

- Dataset loading confirmation
- Dataset shape
- Missing value summary
- Duplicate row summary
- Baseline DiD model summary
- Full controlled model summary
- Backward p-value feature-selection steps
- Final selected model summary
- Model comparison table
- Final DiD estimate
- Final policy interpretation

The script also displays the final Difference-in-Differences policy-impact visualization.

---

## Git Workflow

Useful Git commands for this project:

```bash
git status
git add .
git commit -m "add minimum wage difference-in-differences project"
git push
```

To check remote changes without pulling them into the local project:

```bash
git fetch
git status
```

---

## Recommended `.gitignore`

```text
.venv/
__pycache__/
.ipynb_checkpoints/
.DS_Store
*.pyc
.env
outputs/
```

---

## Author Profile

**Emmanuel Daniel Chonza** is a Monitoring, Evaluation, Learning, Data Science, and Applied Econometrics professional with extensive experience in programme performance measurement, results-based management, data systems, statistical analysis, and evidence-informed decision-making across development programmes in Sub-Saharan Africa.

His work combines applied econometrics, causal inference, machine learning, business analytics, development programme monitoring and evaluation, and policy-focused data analysis.

### Professional Focus

- Monitoring, Evaluation, Accountability and Learning
- Results-Based Management
- Programme performance measurement
- Data analytics and statistical modeling
- Econometrics and causal inference
- Machine learning for business and policy applications
- Development programme analytics
- Evidence-based decision support
- Policy and impact evaluation
- Data visualization and analytical reporting

### Areas of Interest

| Area | Focus |
|---|---|
| Applied Econometrics | Estimating policy and programme effects using statistical models |
| Causal Inference | Applying Difference-in-Differences, propensity score matching, and impact evaluation techniques |
| Machine Learning | Building predictive models for classification, regression, and decision support |
| Data Science for Development | Applying analytics to development-sector and public-policy challenges |
| Monitoring and Evaluation | Strengthening indicators, baselines, targets, reporting, and learning systems |
| Results-Based Management | Linking activities, outputs, outcomes, impacts, and adaptive management |
| Business Analytics | Translating data into insights for operational and strategic decisions |
| Data Visualization | Communicating findings through clear and decision-oriented visuals |

---

## Contact

**Author:** Emmanuel Daniel Chonza  

**LinkedIn:** [Emmanuel Daniel Chonza](https://www.linkedin.com/in/emmanuel-daniel-chonza-b2a0b620/)  

**GitHub:** [chonzadaniel](https://github.com/chonzadaniel)  

**Email:** `chonzadaniel@yahoo.com`

---

## Suggested Citation

Chonza, E. D. (2026). *Difference-in-Differences Minimum Wage Analysis Using Python*. Applied Econometrics and Research Techniques Project.

---

## License

This project is licensed under the **MIT License**.

You are free to use, modify, distribute, and adapt the code, provided that the original license terms are retained.

---

## Conclusion

This project demonstrates how Difference-in-Differences can be implemented in Python to evaluate a real-world policy intervention.

By comparing New Jersey and Pennsylvania before and after the April 1992 minimum wage increase, the project estimates whether the policy was associated with a relative change in fast-food restaurant employment.

The final Difference-in-Differences estimate is approximately:

```text
+2.68 full-time equivalent employees
```

Overall, the analysis provides **no evidence that the minimum wage increase reduced fast-food employment in New Jersey**.

Instead, the results suggest that New Jersey employment increased relative to Pennsylvania after the minimum wage increase.

The project demonstrates how applied econometrics and Python-based linear regression modeling can support evidence-based policy analysis, decision-making, and communication of causal inference results.