"""Build the human-biology teaching notebook; data stays in its original UCI form."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
nb = nbf.v4.new_notebook()
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s.strip()))
def code(s): cells.append(nbf.v4.new_code_cell(s.strip()))

md('''# Human biology: turn a question into a small analysis tool

**Faculty workshop • 20–25 minutes • CPU only • no AI account needed to run**

We will inspect real human measurements, make plots, and use a reusable explorer. An AI assistant can help us change the tool; the data and calculations remain visible in this notebook.

**Teaching questions**

1. What do age, resting blood pressure, and cholesterol look like in these records?
2. How does serum cholesterol differ between the two recorded angiographic-status groups? How much does that estimate vary if we resample the records?
3. Does the comparison look the same within age bands? What can observational data tell us, and what would require a different study?

**Run it:** In your **CloudBank Classroom JupyterHub**, upload or unpack the full workshop folder, open `notebooks/01_human_biology.ipynb`, select its Python kernel, and run cells from top to bottom. Jupyter also provides **Kernel → Restart Kernel and Run All Cells**. The folder includes cached data so the analysis works without a download. Local Jupyter and Google Colab are portable alternatives; a notebook uploaded without its data folder makes one small UCI download. Each code cell has a ▶ button so you can step through the activity.

**Stop and predict:** Before seeing a plot, write one sentence about the age–cholesterol relationship you expect. Then list one reason that expectation could be wrong.''')

md('''## Where the records come from

The **processed Cleveland subset** of [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease) has **303 records**, 13 features, and an angiographic-status field. These are historical clinical observations, not a random sample of today's population. A row represents a patient record. We use the processed file, which does not contain names or identifiers.

**Attribution:** Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository. [DOI: 10.24432/C52P4X](https://doi.org/10.24432/C52P4X). The Cleveland investigator was **Robert Detrano**. UCI distributes the dataset under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The cached raw file is unchanged; below we add readable labels and derived age bands.

This is an exercise in description and critical reading. It does not evaluate or recommend treatment, estimate an individual's risk, or provide a diagnostic tool.''')

md('''## 1. Set up the tools

CloudBank Classroom notebook images vary. Your facilitator should prepare the Python environment before class. This cell checks for core packages; installation is **off by default** to respect a managed JupyterHub environment. If your facilitator enables it, it installs only missing packages and leaves existing packages unchanged. The optional dropdowns use `ipywidgets`; if they cannot display, the explorer also works by changing two words in a function call.''')
code('''import importlib.util
import subprocess
import sys

INSTALL_MISSING = False  # Facilitator may enable in an environment that permits pip installation.
packages = {"numpy": "numpy", "pandas": "pandas", "matplotlib": "matplotlib"}
missing = [package for module, package in packages.items() if importlib.util.find_spec(module) is None]
if missing and not INSTALL_MISSING:
    raise RuntimeError("Missing packages: " + ", ".join(missing) + ". Ask the facilitator to prepare the kernel, or enable INSTALL_MISSING if permitted.")
if missing and INSTALL_MISSING:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + missing)

from pathlib import Path
from urllib.request import urlopen
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

plt.rcParams.update({"figure.figsize": (8, 4.8), "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 11})
print("Ready:", "Python", sys.version.split()[0], "| pandas", pd.__version__, "| NumPy", np.__version__)''')

md('''## 2. Read and validate the data

The loader first looks for the supplied cache from common notebook launch folders. If it is absent, it downloads the same small UCI file. A checksum detects an unexpected source change. **Never let an AI assistant silently replace the data when a download fails.**

Missing values in the source are `?`. We tell pandas to interpret them as missing, rather than as words or zeros.''')
code('''SOURCE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
EXPECTED_SHA256 = "a74b7efa387bc9d108d7d0115d831fe9b414b29ae7124f331b622b4efa0427c8"
filename = "processed.cleveland.data"
candidates = [Path("../data/human_biology") / filename,
              Path("data/human_biology") / filename,
              Path("workshop/data/human_biology") / filename]
data_path = next((p for p in candidates if p.exists()), None)
if data_path is None:
    data_path = Path("data/human_biology") / filename
    data_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urlopen(SOURCE_URL, timeout=45) as response:
            payload = response.read()
    except Exception as error:
        raise RuntimeError("Download failed. Use the workshop folder with its data cache, then rerun this cell.") from error
    if hashlib.sha256(payload).hexdigest() != EXPECTED_SHA256:
        raise ValueError("UCI file differs from the verified workshop copy. Ask the facilitator to inspect the change.")
    data_path.write_bytes(payload)

payload = data_path.read_bytes()
if hashlib.sha256(payload).hexdigest() != EXPECTED_SHA256:
    raise ValueError("Cached dataset checksum mismatch. Restore the original workshop data file.")

COLUMNS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
df = pd.read_csv(data_path, header=None, names=COLUMNS, na_values="?")
if df.shape != (303, 14) or set(df["num"].unique()) != {0, 1, 2, 3, 4}:
    raise ValueError("Unexpected dataset shape or status codes; check the source before analysis.")
print(f"Loaded {len(df)} records from {data_path.resolve()}")
display(df.head())''')

md('''## 3. Translate column names before interpreting a chart

Codes are not automatically measurements. For example, a mean of chest-pain codes would have no clear meaning. The historical `sex` field uses a binary encoding; it is not a complete description of sex or gender. We retain it for provenance and do not use it in this exercise.

UCI does **not** give a unit for maximum achieved heart rate or ST depression in its variable table. We therefore keep those labels explicit instead of having an AI invent units. Our main analyses use variables with documented units.''')
code('''dictionary = pd.DataFrame([
    ("age", "Age", "years; numeric"),
    ("trestbps", "Resting blood pressure on hospital admission", "mm Hg; numeric"),
    ("chol", "Serum cholesterol", "mg/dL; numeric"),
    ("thalach", "Maximum heart rate achieved", "unit not specified by UCI; numeric"),
    ("oldpeak", "Exercise-induced ST depression relative to rest", "unit not specified by UCI; numeric"),
    ("sex", "Historical sex code", "0 = female, 1 = male; categorical"),
    ("cp", "Chest-pain type", "1 typical, 2 atypical, 3 non-anginal, 4 asymptomatic; categorical"),
    ("fbs", "Fasting blood sugar above 120 mg/dL", "0 no, 1 yes; categorical"),
    ("restecg", "Resting ECG category", "0 normal, 1 ST-T abnormality, 2 probable/definite LV hypertrophy; categorical"),
    ("exang", "Exercise-induced angina", "0 no, 1 yes; categorical"),
    ("slope", "Peak exercise ST-segment slope", "1 up, 2 flat, 3 down; categorical"),
    ("ca", "Major vessels visible by fluoroscopy", "count 0–3; may be missing"),
    ("thal", "Scan-result code", "3 normal, 6 fixed defect, 7 reversible defect; may be missing"),
    ("num", "Recorded angiographic-status code", "0 absence, 1–4 presence according to UCI; not used as a numeric score"),
], columns=["column", "meaning", "unit / coding"])
with pd.option_context("display.max_colwidth", None, "display.max_rows", 20):
    display(dictionary)

ABSENT, PRESENT = "Recorded absence", "Recorded presence"
df["status"] = np.where(df["num"].eq(0), ABSENT, PRESENT)
df["age_band"] = pd.cut(df["age"], bins=[0, 45, 55, 65, np.inf],
                        labels=["Under 45", "45–54", "55–64", "65+"], right=False)
LABELS = {"age": "Age (years)", "trestbps": "Resting blood pressure (mm Hg)",
          "chol": "Serum cholesterol (mg/dL)",
          "thalach": "Maximum achieved heart rate (unit unspecified)"}
NUMERIC = list(LABELS)
COLORS = {ABSENT: "#287e8e", PRESENT: "#c76542"}''')

md('''## 4. Inspect missingness and distributions

Look for missing values, unusual values, group imbalance, and spread before summarizing. We keep every record; a chart excludes only rows missing the specific fields it needs. Dropping all rows that contain *any* missing field would discard records unnecessarily.

**Discuss:** Does a high cholesterol observation automatically mean an error? What source or domain information would help you decide?''')
code('''missingness = pd.DataFrame({"missing_n": df[COLUMNS].isna().sum(),
                            "missing_percent": df[COLUMNS].isna().mean().mul(100).round(2)})
display(missingness)
display(df[NUMERIC].describe().round(2))
display(df.groupby("status", sort=False).agg(records=("age", "size"), mean_age=("age", "mean")).round(2))

fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
for ax, variable in zip(axes, ["age", "trestbps", "chol"]):
    ax.hist(df[variable].dropna(), bins=15, color="#287e8e", edgecolor="white")
    ax.set(xlabel=LABELS[variable], ylabel="Records", title=f"n = {df[variable].notna().sum()}")
fig.suptitle("Historical Cleveland records: three measurements", y=1.04)
fig.tight_layout()
plt.show()''')

md('''## 5. Compare groups, with uncertainty

We compare cholesterol using a boxplot (middle line = median; box = middle half; whiskers follow the usual 1.5 × interquartile-range rule; dots outside are plotted observations). The code also reports means and a **bootstrap interval for the difference of means**, defined as recorded presence minus recorded absence.

The bootstrap repeatedly resamples **within each group**, with a fixed random seed. Its interval describes sampling variation under an exchangeable-record assumption. It does not correct selection bias, confounding, the age of the data, or differences in measurement. It is not a reliable population or causal estimate merely because an interval appears precise.''')
code('''groups = [ABSENT, PRESENT]
chol_groups = [df.loc[df["status"].eq(group), "chol"].dropna().to_numpy() for group in groups]
group_summary = df.groupby("status")["chol"].agg(["count", "mean", "median", "std"]).reindex(groups)
display(group_summary.round(2))

fig, ax = plt.subplots()
box = ax.boxplot(chol_groups, patch_artist=True, widths=0.5)
ax.set_xticks([1, 2])
ax.set_xticklabels(groups)
for patch, group in zip(box["boxes"], groups):
    patch.set_facecolor(COLORS[group]); patch.set_alpha(0.65)
ax.set(ylabel=LABELS["chol"], title="Cholesterol by recorded angiographic status")
fig.tight_layout()
plt.show()

rng = np.random.default_rng(2026)
replicates = 2000
boot_absent = rng.choice(chol_groups[0], size=(replicates, len(chol_groups[0])), replace=True).mean(axis=1)
boot_present = rng.choice(chol_groups[1], size=(replicates, len(chol_groups[1])), replace=True).mean(axis=1)
bootstrap_difference = boot_present - boot_absent
observed_difference = chol_groups[1].mean() - chol_groups[0].mean()
low, high = np.quantile(bootstrap_difference, [0.025, 0.975])
print(f"Difference of means (presence − absence): {observed_difference:.2f} mg/dL")
print(f"Exploratory 95% percentile bootstrap interval: [{low:.2f}, {high:.2f}] mg/dL")
print("An interval spanning zero does not demonstrate equivalence; it shows uncertainty in this comparison.")''')

md('''## 6. Ask whether age could affect the comparison

Age could be associated with both the measurement and the recorded status. This makes it a **potential confounder**, not proof that it explains the difference. Compare age-band means and counts with the pooled comparison above. Small groups can be noisy.

Stratification here is a teaching illustration, not a complete adjustment. These broad bands retain age differences within bands; clinical selection, medications, and other unmeasured factors may still matter.''')
code('''age_summary = df.groupby(["age_band", "status"], observed=True)["chol"].agg(["count", "mean", "median"])
display(age_summary.round(2))
age_means = age_summary["mean"].unstack("status").reindex(columns=groups)
age_counts = age_summary["count"].unstack("status").reindex(columns=groups)
stratified = pd.DataFrame({"absence_n": age_counts[ABSENT], "presence_n": age_counts[PRESENT],
                          "mean_difference_mg_dL": age_means[PRESENT] - age_means[ABSENT]})
display(stratified.round(2))
ax = age_means.plot(marker="o", color=[COLORS[g] for g in groups])
ax.set(xlabel="Age band (years)", ylabel="Mean cholesterol (mg/dL)",
       title="Age-band comparisons; inspect the counts above")
ax.legend(title="Recorded status")
plt.tight_layout()
plt.show()''')

md('''## 7. Turn the analysis into an interactive tool

The next cell defines `explore`: a reusable function. Its inputs are column names, an age range, and a choice of group colors. It reports the number of usable records and a Pearson correlation, then draws a scatterplot. The line is a simple least-squares descriptive fit across the filtered records; it has no predictive or causal interpretation.

**Try three changes separately:** change cholesterol to blood pressure; filter the age range; then turn grouping off. Keep a note of the change and what you learned. Choosing x = y produces the same value on both axes, so the tool asks you to choose different variables.''')
code('''def explore(x="age", y="chol", age_range=(29, 77), color_by_status=True):
    if x not in LABELS or y not in LABELS:
        raise ValueError("Choose a numeric column from: " + ", ".join(LABELS))
    if x == y:
        print("Choose different variables for x and y.")
        return None
    if len(age_range) != 2 or age_range[0] > age_range[1]:
        raise ValueError("Age range must be (minimum, maximum) with minimum <= maximum.")
    selected = df.loc[df["age"].between(age_range[0], age_range[1])].copy()
    usable = selected.dropna(subset=[x, y])
    excluded = len(selected) - len(usable)
    print(f"Age range {age_range[0]}–{age_range[1]}: {len(usable)} usable records; {excluded} excluded for missing plotted values.")
    if len(usable) < 3 or usable[x].nunique() < 2 or usable[y].nunique() < 2:
        print("Too few records or too little variation for a correlation/fit. Expand the range.")
        return None
    correlation = usable[x].corr(usable[y])
    print(f"Pearson r = {correlation:.3f}; descriptive association in this filtered sample.")
    fig, ax = plt.subplots(figsize=(8.5, 5))
    if color_by_status:
        for group in groups:
            subset = usable.loc[usable["status"].eq(group)]
            ax.scatter(subset[x], subset[y], alpha=0.6, s=25, color=COLORS[group], label=f"{group} (n={len(subset)})")
        ax.legend(fontsize=9)
    else:
        ax.scatter(usable[x], usable[y], alpha=0.6, s=25, color="#287e8e")
    slope, intercept = np.polyfit(usable[x], usable[y], 1)
    grid = np.linspace(usable[x].min(), usable[x].max(), 100)
    ax.plot(grid, slope * grid + intercept, color="#333333", linestyle="--", label="Descriptive pooled fit")
    ax.set(xlabel=LABELS[x], ylabel=LABELS[y], title=f"Explore {x} and {y} | n={len(usable)}, r={correlation:.2f}")
    fig.tight_layout()
    plt.show()
    return {"n": len(usable), "excluded_missing": excluded, "pearson_r": float(correlation), "x": x, "y": y}

# This call also works if your notebook cannot display widgets.
explorer_result = explore(x="age", y="chol", age_range=(29, 77), color_by_status=True)''')
code('''# The function call above remains available if the hub has no widget support.
try:
    import ipywidgets as widgets
    controls = {
        "x": widgets.Dropdown(options=[(LABELS[k], k) for k in NUMERIC], value="age", description="x:"),
        "y": widgets.Dropdown(options=[(LABELS[k], k) for k in NUMERIC], value="chol", description="y:"),
        "age_range": widgets.IntRangeSlider(value=(29, 77), min=29, max=77, description="Age:", continuous_update=False),
        "color_by_status": widgets.Checkbox(value=True, description="Color by status")
    }
    widget_output = widgets.interactive_output(explore, controls)
    display(widgets.VBox(list(controls.values())), widget_output)
except Exception as error:
    print("Widget display unavailable. Use explore(x='age', y='chol', age_range=(29, 77)) above.")
    print(type(error).__name__ + ": " + str(error))''')

md('''## 8. Practice asking an AI for a small, checkable change

Copy a relevant cell and the dataset dictionary into your assistant. Make **one change at a time**, then rerun the modified cell and a known example. Ask the assistant to explain its assumptions; inspect the changed lines.

**Prompt A — change one visual choice**

> In this Python notebook, update only the `explore` function to use a larger font suitable for a lecture screen. Keep its input arguments, missing-value handling, reported n, and scientific interpretation. Show the full replacement cell and explain the two lines you changed.

**Prompt B — add a new descriptive question**

> Add a cell that summarizes resting blood pressure (`trestbps`, mm Hg) by the existing `age_band` categories. Report count, mean, and median; label the plot with units. Use `df` without modifying it. Do not add a causal claim or a medical threshold. State one limitation and how I can check the calculation using a small subset.

**Prompt C — challenge the interpretation**

> Review this claim: “Higher cholesterol causes the recorded heart disease in these data.” Use the notebook's source description and analysis to identify what is observed, what is inferred, and what the study cannot establish. Write a replacement sentence tied to the displayed numbers. Do not invent a result.

**Prompt D — revise the reusable tool**

> Modify `explore` to let me choose a histogram instead of a scatterplot. Before writing code, list which parameters need different meanings and propose a simple interface. Keep the original scatterplot behavior working. Explain how I can check missing data and labels in both modes.

**Check every AI change:** Does it run? Does it use the intended rows and variables? Are units documented? Does the reported n match? Does its written claim follow from the displayed calculation?''')

md('''## 9. Save an artifact and write a cautious result

This cell creates a portable summary and a static plot in the current runtime's `outputs/01_human_biology/` folder. Your JupyterHub file browser lets you download them. Your saved notebook captures the reasoning as well as the chart.

Complete this sentence with the actual results shown above:

> “In these 303 historical Cleveland records, the mean serum cholesterol difference between the recorded presence and absence groups was ___ mg/dL, with an exploratory bootstrap interval of ___. The age-band comparisons suggest ___. This does not establish ___ because ___.”

**Exit ticket:** Name one data check, one AI-generated change you verified, and one follow-up study or measurement you would need before making a causal claim.''')
code('''output_dir = Path("outputs/01_human_biology")
output_dir.mkdir(parents=True, exist_ok=True)
group_summary.to_csv(output_dir / "cholesterol_group_summary.csv")
stratified.to_csv(output_dir / "age_band_comparison.csv")
missingness.to_csv(output_dir / "missingness.csv")

fig, ax = plt.subplots(figsize=(8, 5))
for group in groups:
    part = df.loc[df["status"].eq(group)]
    ax.scatter(part["age"], part["chol"], alpha=0.6, s=25, color=COLORS[group], label=f"{group} (n={len(part)})")
ax.set(xlabel=LABELS["age"], ylabel=LABELS["chol"], title="Historical Cleveland observations; association only")
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(output_dir / "age_cholesterol.png", dpi=160)
plt.close(fig)
print("Saved:")
for path in sorted(output_dir.iterdir()):
    print(" •", path.resolve())''')

md('''## References and reuse

- [UCI dataset page, variable descriptions, citation, and CC BY 4.0 license](https://archive.ics.uci.edu/dataset/45/heart+disease).
- [Original processed Cleveland data](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data).
- [Original UCI documentation and investigator attribution](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/heart-disease.names).
- [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/).

For a different class, [UCI Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) supplies 299 records with numeric ejection fraction, serum creatinine, sodium, and age (CC BY 4.0). Its follow-up duration requires special care for survival questions; a death-event classifier that ignores unequal follow-up can be misleading. This backup dataset is not loaded by this notebook.''')

nb.cells = cells
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
               "language_info": {"name": "python", "version": "3.8"},
               "colab": {"name": "01_human_biology.ipynb", "provenance": []}}
path = ROOT / "notebooks/01_human_biology.ipynb"
nbf.write(nb, str(path))
print("Wrote", path, "with", len(cells), "cells")
