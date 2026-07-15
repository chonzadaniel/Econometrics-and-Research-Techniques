# Difference-in-Differences Minimum Wage Analysis Report

## 1. Problem Statement

The April 1992 minimum wage increase in New Jersey created an important labour-market policy question: **did the increase in the minimum wage reduce employment in fast-food restaurants?**

A common economic concern is that increasing the minimum wage may raise labour costs and cause firms to reduce employment. However, actual employment responses may differ depending on market structure, consumer demand, pricing strategies, worker productivity, firm-level adjustment mechanisms, and the ability of businesses to absorb higher wage costs.

This project evaluates the employment effect of the New Jersey minimum wage increase by comparing fast-food restaurants in:

- **New Jersey**, the treatment group affected by the minimum wage increase; and
- **Pennsylvania**, the comparison group not affected by the same policy change.

The outcome variable is **full-time equivalent employment**, represented by `fte`.

The central question is whether employment in New Jersey changed differently after the minimum wage increase compared with Pennsylvania.

---

## 2. Objective

The main objective of this project is to estimate the impact of the April 1992 New Jersey minimum wage increase on fast-food restaurant employment using a **Difference-in-Differences linear regression framework**.

Specific objectives are to:

1. Load and prepare the minimum wage dataset for econometric modeling.
2. Define the treatment group, comparison group, pre-policy period, and post-policy period.
3. Construct the Difference-in-Differences interaction term.
4. Estimate a baseline Difference-in-Differences model.
5. Estimate additional linear regression models with control variables.
6. Use p-value based model refinement to remove statistically insignificant controls.
7. Preserve the core Difference-in-Differences variables throughout the modeling process.
8. Estimate the final selected model.
9. Visualize the observed and counterfactual employment paths.
10. Interpret the policy and business implications of the final treatment-effect estimate.

---

## 3. Methodology

This project applies the **Difference-in-Differences** method, an econometric approach used to estimate the effect of an intervention by comparing outcome changes over time between a treatment group and a comparison group.

The treatment group is:

```text
New Jersey restaurants
```

The comparison group is:

```text
Pennsylvania restaurants
```

The intervention is:

```text
April 1992 New Jersey minimum wage increase
```

The outcome is:

```text
Full-time equivalent employment
```

The baseline Difference-in-Differences model is specified as:

$$
FTE_i
=
\beta_0
+
\beta_1 NJ_i
+
\beta_2 POST_i
+
\beta_3(NJ_i \times POST_i)
+
\varepsilon_i
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

This coefficient measures whether employment in New Jersey changed differently after the minimum wage increase compared with the Pennsylvania counterfactual trend.

---

## 4. Data Preparation

The dataset used in this project is:

```text
njmin3.csv
```

The data preparation process included the following steps:

1. Loaded the dataset into Python.
2. Reviewed column names and basic dataset structure.
3. Checked for missing values.
4. Checked for duplicate records.
5. Removed duplicate rows where applicable.
6. Removed observations with missing `fte` values, because `fte` is the dependent variable.
7. Converted relevant variables to numeric format where needed.
8. Recreated the Difference-in-Differences interaction term:

```python
NJ_POST_APRIL92 = NJ * POST_APRIL92
```

The main modeling variables were:

| Variable | Role |
|---|---|
| `fte` | Outcome variable |
| `NJ` | Treatment-group indicator |
| `POST_APRIL92` | Post-policy indicator |
| `NJ_POST_APRIL92` | Difference-in-Differences treatment-effect variable |

Additional control variables considered in the modeling process included restaurant chain, ownership, and regional indicators.

---

## 5. Modeling Results

### 5.1 Baseline Difference-in-Differences Model

The first model estimated the basic Difference-in-Differences specification:

```text
fte ~ NJ + POST_APRIL92 + NJ_POST_APRIL92
```

This model included only the three core Difference-in-Differences variables:

| Variable | Purpose |
|---|---|
| `NJ` | Captures baseline differences between New Jersey and Pennsylvania |
| `POST_APRIL92` | Captures time-period changes after April 1992 |
| `NJ_POST_APRIL92` | Captures the treatment effect of the minimum wage increase |

The coefficient on `NJ_POST_APRIL92` is the key estimate. It measures the relative change in New Jersey employment after the policy compared with Pennsylvania.

The baseline model indicated a **positive Difference-in-Differences estimate**, suggesting that New Jersey employment did not fall relative to Pennsylvania after the minimum wage increase.

---

### 5.2 Full Linear Regression Model with Controls

The second model added control variables to account for observable restaurant-level differences.

The full model followed the structure:

```text
fte ~ NJ + POST_APRIL92 + NJ_POST_APRIL92 + controls
```

The controls considered included:

| Control Type | Example Variables |
|---|---|
| Restaurant chain | `bk`, `kfc`, `roys`, `wendys` |
| Ownership type | `co_owned` |
| Regional indicators | `centralj`, `southj`, `pa1`, `pa2` |

The purpose of adding controls was to improve the model specification by accounting for observable differences that could influence employment levels independently of the minimum wage policy.

The full controlled model still retained the core Difference-in-Differences variables because those variables define the policy evaluation design.

---

### 5.3 P-Value Based Feature Selection

After estimating the full model, a backward p-value based feature-selection process was applied.

The process worked as follows:

1. Fit the full model with all candidate controls.
2. Identify the control variable with the highest p-value.
3. Remove the least statistically significant control variable if its p-value exceeded the selected significance threshold.
4. Refit the model.
5. Repeat the process until all remaining control variables were statistically relevant or no removable controls remained.

The following core Difference-in-Differences variables were protected and never removed:

```text
NJ
POST_APRIL92
NJ_POST_APRIL92
```

These variables were protected because removing them would break the causal structure of the Difference-in-Differences design.

Only optional control variables were eligible for removal.

---

### 5.4 Final Selected Model

The final selected model retained the core Difference-in-Differences variables and only the control variables that remained after p-value based refinement.

The final model provided the most focused specification because it:

- Preserved the Difference-in-Differences research design;
- Removed statistically weak controls;
- Retained the key policy-impact variable;
- Produced an interpretable estimate of the minimum wage effect.

The final model continued to show a **positive coefficient** on `NJ_POST_APRIL92`.

This means that the estimated employment change in New Jersey after the policy was higher than the estimated counterfactual based on Pennsylvania’s trend.

---

## 6. Final Results

The final Difference-in-Differences estimate was approximately:

```text
+2.68 FTE employees
```

This means that, after the April 1992 minimum wage increase, New Jersey fast-food restaurants had approximately **2.68 more full-time equivalent employees** relative to the Pennsylvania counterfactual trend.

### Interpretation of the Final DiD Estimate

The coefficient on `NJ_POST_APRIL92` represents the estimated treatment effect.

Because the coefficient is positive, the model suggests that:

```text
New Jersey employment increased relative to Pennsylvania after the minimum wage increase.
```

The result does **not** support the claim that the minimum wage increase reduced fast-food employment in New Jersey.

Instead, the estimated effect suggests that employment was higher in New Jersey than what would have been expected if New Jersey had followed the Pennsylvania trend.

---

## 7. Final DiD Visualization Interpretation

The final Difference-in-Differences visualization compares three employment paths:

| Series | Meaning |
|---|---|
| Observed PA | Actual employment trend in Pennsylvania |
| Observed NJ | Actual employment trend in New Jersey |
| Counterfactual NJ | Estimated New Jersey employment trend if New Jersey had followed Pennsylvania’s pattern |

The most important visual feature is the vertical gap between:

```text
Observed post-policy New Jersey employment
```

and:

```text
Counterfactual post-policy New Jersey employment
```

That vertical gap represents the estimated Difference-in-Differences treatment effect.

The visualization shows that the observed New Jersey post-policy employment level lies above the counterfactual New Jersey line.

This supports the regression result that the minimum wage increase was not associated with a relative employment decline in New Jersey.

---

## 8. Business and Policy Recommendations

### 8.1 Avoid Assuming Minimum Wage Increases Automatically Reduce Employment

The modeling results do not support the assumption that the April 1992 New Jersey minimum wage increase reduced fast-food employment.

Decision-makers should therefore avoid making automatic conclusions that minimum wage increases necessarily lead to job losses.

---

### 8.2 Use Evidence-Based Policy Evaluation

Labour-market policy decisions should be supported by empirical analysis. Difference-in-Differences provides a useful framework for comparing affected and unaffected groups before and after policy changes.

For future policy evaluation, decision-makers should continue using structured causal inference methods rather than relying only on theoretical expectations.

---

### 8.3 Consider Business Adjustment Mechanisms

The absence of a negative employment effect suggests that restaurants may have adjusted to higher wages through mechanisms other than reducing employment.

Possible adjustment mechanisms may include:

- Small price increases;
- Higher worker productivity;
- Reduced employee turnover;
- Improved scheduling efficiency;
- Absorbing costs through margins;
- Increased consumer demand;
- Operational restructuring.

This means employment is only one part of the business response to wage policy.

---

### 8.4 Strengthen Future Analysis with More Data

Future evaluations would be stronger if they include:

- More pre-policy time periods;
- More post-policy periods;
- Store-level fixed effects;
- Time fixed effects;
- Wage data;
- Price data;
- Revenue and profit measures;
- Employee turnover indicators;
- Alternative comparison states;
- Sensitivity checks.

These additions would strengthen confidence in the estimated policy effect.

---

### 8.5 Interpret the Results Within the Parallel Trends Assumption

The Difference-in-Differences estimate depends on the assumption that, without the policy change, New Jersey employment would have followed a similar trend to Pennsylvania.

Therefore, the results should be interpreted as credible within the limits of the parallel trends assumption.

Policy decisions should consider this assumption when using the findings.

---

## 9. Conclusion

This project applied a Difference-in-Differences linear regression framework to evaluate the employment effect of the April 1992 New Jersey minimum wage increase.

The final model showed a positive treatment-effect estimate of approximately:

```text
+2.68 full-time equivalent employees
```

The final visualization also showed that observed New Jersey employment after the policy was higher than the estimated counterfactual employment level.

Overall, the analysis provides **no evidence that the minimum wage increase reduced fast-food employment in New Jersey**.

Instead, the results suggest that New Jersey employment increased relative to Pennsylvania after the minimum wage increase.

The project demonstrates how applied econometrics and Python-based linear regression modeling can be used to evaluate public policy interventions, support evidence-based decision-making, and communicate causal inference results through both statistical models and visual interpretation.