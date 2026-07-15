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
| β₀ | Intercept |
| β₁ | Baseline difference between New Jersey and Pennsylvania |
| β₂ | Time-period difference before and after the policy |
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