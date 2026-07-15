# Difference-in-Differences: Minimum Wage Project
# End-to-End Python Script for VS Code
# Purpose:
# Estimate the impact of the April 1992 New Jersey minimum wage increase
# on fast-food restaurant employment using Difference-in-Differences.

# ============================================================
# 1. Import Required Libraries
# ============================================================

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

warnings.filterwarnings("ignore")


# ============================================================
# 2. Load Dataset
# ============================================================

# The script checks whether the dataset is in the project root or in a data folder.
PROJECT_DIR = Path.cwd()

DATA_PATH_OPTIONS = [
    PROJECT_DIR / "njmin3.csv",
    PROJECT_DIR / "data" / "njmin3.csv"
]

DATA_PATH = None

for path in DATA_PATH_OPTIONS:
    if path.exists():
        DATA_PATH = path
        break

if DATA_PATH is None:
    raise FileNotFoundError(
        "The dataset 'njmin3.csv' was not found. "
        "Please place it in the project root or inside a folder named 'data'."
    )

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully.")
print(f"Dataset path: {DATA_PATH}")
print(f"Dataset shape: {df.shape}")


# ============================================================
# 3. Basic Data Quality Checks and Cleaning
# ============================================================

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values before cleaning:")
print(df.isna().sum())

print("\nDuplicate rows before cleaning:")
print(df.duplicated().sum())

# Remove duplicate rows if any exist.
initial_rows = df.shape[0]
df = df.drop_duplicates().copy()
removed_duplicates = initial_rows - df.shape[0]

print(f"\nDuplicate rows removed: {removed_duplicates}")

# Ensure the key DiD interaction term exists and is correctly defined.
required_base_columns = ["NJ", "POST_APRIL92", "fte"]

missing_base_columns = [
    col for col in required_base_columns if col not in df.columns
]

if missing_base_columns:
    raise ValueError(
        f"The following required columns are missing: {missing_base_columns}"
    )

# Recreate the interaction term to avoid relying on any pre-existing incorrect value.
df["NJ_POST_APRIL92"] = df["NJ"] * df["POST_APRIL92"]

# Drop observations with missing outcome because OLS requires a valid dependent variable.
# This is preferred to imputing the outcome variable in a causal model.
rows_before_outcome_cleaning = df.shape[0]
df = df.dropna(subset=["fte"]).copy()
rows_removed_missing_fte = rows_before_outcome_cleaning - df.shape[0]

print(f"Rows removed due to missing fte outcome: {rows_removed_missing_fte}")

# Convert all model columns to numeric where possible.
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nMissing values after basic cleaning:")
print(df.isna().sum())

print(f"\nFinal modeling dataset shape: {df.shape}")


# ============================================================
# 4. Define Outcome, Treatment, Post, Interaction, and Controls
# ============================================================

# Outcome variable
OUTCOME = "fte"

# Core Difference-in-Differences variables
TREATMENT = "NJ"
POST = "POST_APRIL92"
DID = "NJ_POST_APRIL92"

# These variables must remain in every model.
# They define the Difference-in-Differences structure.
core_features = [
    TREATMENT,
    POST,
    DID
]

# Optional control variables available in the dataset.
# These controls account for restaurant chain, ownership, and region differences.
candidate_controls = [
    "bk",
    "kfc",
    "roys",
    "wendys",
    "co_owned",
    "centralj",
    "southj",
    "pa1",
    "pa2"
]

# Keep only controls that exist in the dataset.
candidate_controls = [
    col for col in candidate_controls if col in df.columns
]

# Create the modeling outcome.
y = df[OUTCOME].copy()

print("\nCore DiD variables:")
print(core_features)

print("\nCandidate control variables:")
print(candidate_controls)


# ============================================================
# 5. Helper Function to Fit OLS DiD Models
# ============================================================

def fit_ols_model(data, outcome, features, model_name):
    """
    Fits an OLS model with a constant term and robust standard errors.

    Parameters
    ----------
    data : pandas.DataFrame
        Modeling dataset.
    outcome : str
        Dependent variable.
    features : list
        Independent variables.
    model_name : str
        Name used for reporting.

    Returns
    -------
    model : statsmodels RegressionResults
        Fitted OLS model.
    """

    X = data[features].copy()
    X = sm.add_constant(X, has_constant="add")

    y_model = data[outcome].copy()

    model = sm.OLS(y_model, X).fit(cov_type="HC1")

    print("\n" + "=" * 80)
    print(model_name)
    print("=" * 80)
    print(model.summary())

    if DID in model.params.index:
        print("\nKey DiD estimate:")
        print(f"{DID} coefficient: {model.params[DID]:.4f}")
        print(f"{DID} p-value    : {model.pvalues[DID]:.4f}")

    return model


# ============================================================
# 6. Model 1: Baseline Difference-in-Differences Model
# ============================================================

# Baseline DiD model:
# fteᵢ = β₀ + β₁NJᵢ + β₂POSTᵢ + β₃(NJᵢ × POSTᵢ) + εᵢ
#
# β₃ is the Difference-in-Differences estimate.

baseline_features = core_features.copy()

model_1 = fit_ols_model(
    data=df,
    outcome=OUTCOME,
    features=baseline_features,
    model_name="Model 1: Baseline Difference-in-Differences Model"
)


# ============================================================
# 7. Model 2: Full Model with All Candidate Controls
# ============================================================

# This model adds available controls to the baseline DiD specification.
# Some controls may be statistically insignificant or collinear.
# The next section removes insignificant controls step by step.

full_features = core_features + candidate_controls

model_2 = fit_ols_model(
    data=df,
    outcome=OUTCOME,
    features=full_features,
    model_name="Model 2: Full Difference-in-Differences Model with All Controls"
)


# ============================================================
# 8. Backward P-Value Based Feature Selection
# ============================================================

# The purpose is to simplify the model by removing statistically insignificant controls.
# The core DiD variables are protected and are not removed:
# - NJ
# - POST_APRIL92
# - NJ_POST_APRIL92
#
# Only control variables are considered for removal.
# The highest p-value control is removed one at a time until all remaining controls
# are statistically significant at the selected threshold.

P_VALUE_THRESHOLD = 0.05

current_features = full_features.copy()
protected_features = core_features.copy()

model_history = []
iteration = 1

print("\n" + "=" * 80)
print("Backward P-Value Based Feature Selection")
print("=" * 80)

while True:
    current_model = sm.OLS(
        y,
        sm.add_constant(df[current_features], has_constant="add")
    ).fit(cov_type="HC1")

    # Store current model results before any variable removal.
    model_history.append({
        "iteration": iteration,
        "features": current_features.copy(),
        "n_features": len(current_features),
        "did_coefficient": current_model.params.get(DID, np.nan),
        "did_p_value": current_model.pvalues.get(DID, np.nan),
        "r_squared": current_model.rsquared,
        "adj_r_squared": current_model.rsquared_adj,
        "aic": current_model.aic,
        "bic": current_model.bic
    })

    # Extract p-values for removable controls only.
    removable_controls = [
        feature for feature in current_features
        if feature not in protected_features
    ]

    control_pvalues = current_model.pvalues[
        current_model.pvalues.index.isin(removable_controls)
    ]

    # Stop if there are no removable controls left.
    if control_pvalues.empty:
        print("\nNo removable control variables remain.")
        final_selected_model = current_model
        break

    # Identify the least significant control variable.
    worst_control = control_pvalues.idxmax()
    worst_pvalue = control_pvalues.max()

    print(
        f"Iteration {iteration}: highest control p-value = "
        f"{worst_pvalue:.4f} for '{worst_control}'"
    )

    # Stop if all remaining controls are statistically significant.
    if worst_pvalue <= P_VALUE_THRESHOLD:
        print("\nAll remaining controls are statistically significant.")
        final_selected_model = current_model
        break

    # Remove the least significant control variable.
    print(f"Removing insignificant control variable: {worst_control}")
    current_features.remove(worst_control)

    iteration += 1


# ============================================================
# 9. Final Selected Model
# ============================================================

final_features = current_features.copy()

final_model = fit_ols_model(
    data=df,
    outcome=OUTCOME,
    features=final_features,
    model_name="Final Selected Difference-in-Differences Model"
)

model_history_df = pd.DataFrame(model_history)

print("\nModel selection history:")
print(
    model_history_df[
        [
            "iteration",
            "n_features",
            "did_coefficient",
            "did_p_value",
            "r_squared",
            "adj_r_squared",
            "aic",
            "bic"
        ]
    ]
)

print("\nFinal selected features:")
print(final_features)


# ============================================================
# 10. Model Comparison Table
# ============================================================

model_comparison = pd.DataFrame({
    "model": [
        "Model 1: Baseline DiD",
        "Model 2: Full controls",
        "Final selected model"
    ],
    "n_features": [
        len(baseline_features),
        len(full_features),
        len(final_features)
    ],
    "did_coefficient": [
        model_1.params.get(DID, np.nan),
        model_2.params.get(DID, np.nan),
        final_model.params.get(DID, np.nan)
    ],
    "did_p_value": [
        model_1.pvalues.get(DID, np.nan),
        model_2.pvalues.get(DID, np.nan),
        final_model.pvalues.get(DID, np.nan)
    ],
    "r_squared": [
        model_1.rsquared,
        model_2.rsquared,
        final_model.rsquared
    ],
    "adj_r_squared": [
        model_1.rsquared_adj,
        model_2.rsquared_adj,
        final_model.rsquared_adj
    ],
    "aic": [
        model_1.aic,
        model_2.aic,
        final_model.aic
    ],
    "bic": [
        model_1.bic,
        model_2.bic,
        final_model.bic
    ]
})

print("\nModel comparison:")
print(model_comparison)


# ============================================================
# 11. Compute DiD Plot Values from the Final Selected Model
# ============================================================

# For plotting, we use the final selected model coefficients.
# The visualization focuses on the core DiD structure:
#
# Pre PA  = β₀
# Post PA = β₀ + β₂
# Pre NJ  = β₀ + β₁
# Post NJ = β₀ + β₁ + β₂ + β₃
#
# The counterfactual NJ post-policy value is:
# Counterfactual NJ = β₀ + β₁ + β₂
#
# The DiD effect is:
# Post NJ - Counterfactual NJ = β₃

params = final_model.params

intercept = params.get("const", 0)
nj_coef = params.get(TREATMENT, 0)
post_coef = params.get(POST, 0)
did_coef = params.get(DID, 0)

pre_pa = intercept
post_pa = intercept + post_coef

pre_nj = intercept + nj_coef
post_nj = intercept + nj_coef + post_coef + did_coef

counterfactual = intercept + nj_coef + post_coef

print("\nFinal model predicted DiD plot values:")
print(f"Pre-policy PA               : {pre_pa:.4f}")
print(f"Post-policy PA              : {post_pa:.4f}")
print(f"Pre-policy NJ               : {pre_nj:.4f}")
print(f"Observed post-policy NJ     : {post_nj:.4f}")
print(f"Counterfactual post-policy NJ: {counterfactual:.4f}")
print(f"DiD effect                  : {post_nj - counterfactual:.4f}")


# ============================================================
# 12. Final Difference-in-Differences Impact Visualization
# ============================================================

sns.set_theme(style="whitegrid", context="notebook")

# Prepare plot data
plot_df = pd.DataFrame({
    "Period": ["Pre-April 1992", "Post-April 1992"] * 3,
    "FTE": [pre_pa, post_pa, pre_nj, post_nj, pre_nj, counterfactual],
    "Series": ["Observed PA"] * 2 + ["Observed NJ"] * 2 + ["Counterfactual NJ"] * 2
})

# Plot observed PA, observed NJ, and counterfactual NJ
plt.figure(figsize=(16, 8))

sns.lineplot(
    data=plot_df,
    x="Period",
    y="FTE",
    hue="Series",
    style="Series",
    markers=True,
    dashes={
        "Observed PA": "",
        "Observed NJ": "",
        "Counterfactual NJ": (3, 2)
    },
    linewidth=2.8,
    markersize=8
)

# Policy intervention marker
plt.axvline(0.5, color="black", linestyle=":", alpha=0.7)

plt.text(
    0.5,
    plot_df["FTE"].max() + 0.5,
    "Minimum wage\nincrease",
    ha="center",
    fontsize=10
)

# Treatment effect gap
plt.vlines(
    x=1,
    ymin=counterfactual,
    ymax=post_nj,
    color="darkgreen",
    linewidth=3
)

# Curved arrow and treatment effect label
plt.annotate(
    f"DiD effect = {post_nj - counterfactual:.2f} FTE",
    xy=(1, post_nj),
    xytext=(0.65, post_nj + 1.5),
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=-0.3",
        color="darkgreen",
        lw=2
    ),
    fontsize=11,
    color="darkgreen",
    fontweight="bold"
)

# Counterfactual label
plt.annotate(
    "Counterfactual NJ",
    xy=(1, counterfactual),
    xytext=(0.62, counterfactual - 1.5),
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=0.25",
        color="blue",
        lw=1.8
    ),
    fontsize=10,
    color="blue"
)

# Titles and labels
plt.title(
    "DiD: Impact of April 1992 Minimum Wage Intervention",
    fontsize=20,
    weight="bold"
)

plt.xlabel("Timeline", fontsize=14, weight="bold")
plt.ylabel("Full-Time Equivalent Employment (FTE)", fontsize=14, weight="bold")
plt.legend(title="Series", bbox_to_anchor=(1.02, 1), loc="upper left")

sns.despine()
plt.tight_layout()
plt.show()


# ============================================================
# 13. Final Interpretation
# ============================================================

did_estimate = final_model.params.get(DID, np.nan)
did_pvalue = final_model.pvalues.get(DID, np.nan)

print("\n" + "=" * 80)
print("Final Interpretation")
print("=" * 80)

print(f"Final selected model DiD estimate: {did_estimate:.4f}")
print(f"Final selected model DiD p-value : {did_pvalue:.4f}")

if did_estimate > 0:
    print(
        "\nThe estimated DiD effect is positive. This suggests that after the April 1992 "
        "minimum wage increase, New Jersey restaurants had higher full-time equivalent "
        "employment relative to the counterfactual trend based on Pennsylvania."
    )
elif did_estimate < 0:
    print(
        "\nThe estimated DiD effect is negative. This suggests that after the April 1992 "
        "minimum wage increase, New Jersey restaurants had lower full-time equivalent "
        "employment relative to the counterfactual trend based on Pennsylvania."
    )
else:
    print(
        "\nThe estimated DiD effect is exactly zero in this model."
    )

if did_pvalue < 0.05:
    print(
        "\nThe DiD estimate is statistically significant at the 5% level."
    )
else:
    print(
        "\nThe DiD estimate is not statistically significant at the 5% level. "
        "This means the evidence should be interpreted cautiously."
    )

print(
    "\nPolicy message: The model estimates whether New Jersey employment changed "
    "differently from Pennsylvania employment after the minimum wage increase. "
    "The DiD coefficient is the key policy-impact estimate."
)