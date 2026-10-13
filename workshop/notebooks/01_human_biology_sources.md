# Human biology notebook: sources and preparation

The notebook fits a 20–25 minute demo/exploration within the 90-minute session. Primary delivery is the user's CloudBank Classroom JupyterHub, with a Python 3 kernel, the full workshop folder, and a CPU environment. CloudBank reference: [Access CloudBank Classroom](https://www.cloudbank.org/training/access-cloudbank-classroom). Exact hub images and preinstalled libraries vary; prepare and run the notebook in the actual classroom image before the session.

## Primary dataset: UCI Heart Disease, processed Cleveland subset

- **Primary source:** [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease).
- **Direct data:** [processed.cleveland.data](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data).
- **Original documentation:** [heart-disease.names](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/heart-disease.names).
- **Citation:** Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository. [DOI 10.24432/C52P4X](https://doi.org/10.24432/C52P4X). Robert Detrano was the principal investigator responsible for the Cleveland data.
- **License:** UCI explicitly states [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Preserve attribution and note changes when redistributing derived results.
- **Size:** 303 patient records, 13 features plus recorded angiographic status. Raw cache is only 18,461 bytes.
- **Documented main units:** age in years; hospital-admission resting blood pressure in mm Hg; serum cholesterol in mg/dL. The source's variable table does not specify units for `thalach` or `oldpeak`, so the notebook explicitly marks those as unspecified rather than assigning undocumented units.
- **Cache:** `../data/human_biology/processed.cleveland.data`, unchanged from UCI; SHA-256 `a74b7efa387bc9d108d7d0115d831fe9b414b29ae7124f331b622b4efa0427c8`.
- **Changes in analysis:** parse `?` as missing; derive a presence/absence status label from `num`; create age bands; retain all original observations. There are 4 missing `ca` values and 2 missing `thal` values. Main numeric variables have no missing values in this file.
- **Teaching questions:** inspect distributions and outliers; compare cholesterol between recorded-status groups; interpret a bootstrap interval; consider age as a possible confounder; build a widget-driven scatterplot explorer.
- **Limitations:** historical clinical selection, limited population coverage, unmeasured confounders, no causal design, broad age bands, and measurement documentation gaps. The original diagnosis codes are not treated as a continuous disease severity scale. The dataset is useful for explaining analysis mechanics, not for providing clinical advice or predicting a participant's risk.

## Backup: UCI Heart Failure Clinical Records

- **Primary source:** [UCI Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records).
- **Citation:** *Heart Failure Clinical Records* [Dataset]. (2020). UCI Machine Learning Repository. [DOI 10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).
- **License:** CC BY 4.0, as explicitly listed by UCI.
- **Size and variables:** 299 clinical records. Numeric examples: age (years), ejection fraction (%), serum creatinine (mg/dL), sodium (mEq/L), and follow-up time (days).
- **Teaching questions:** How do ejection fraction and serum creatinine vary? Does their association change when stratified by age? How does a histogram respond to a log scale for a skewed biomarker?
- **Why it is a backup:** clear units and small file, but mortality outcomes can be emotionally sensitive and survival analysis requires accounting for unequal follow-up. Avoid a simple death-event classifier that includes follow-up duration as a baseline predictor or ignores censoring. Use biomarker description for a beginner session.
- **Implementation status:** verified candidate only; not downloaded or implemented in the core notebook.

## Minimal environment and usage

Core: `numpy`, `pandas`, `matplotlib`; optional controls: `ipywidgets`; notebook runtime: `ipykernel` in JupyterHub or Jupyter. No scipy, seaborn, scikit-learn, model download, GPU, API key, or Hugging Face account is required. Use Python 3.10+ for the classroom environment. The notebook also runs with the older system Python 3.8 used for a compatibility check.

Installation is off by default (`INSTALL_MISSING = False`). Prepare packages through the classroom administrator or set that flag only if pip installation is appropriate for the supplied kernel. Widgets can be omitted; `explore(...)` is the same analysis function and serves as a reliable fallback.

The core runs offline when packages and the cache are present. Launching from the repo root, `workshop/`, or `workshop/notebooks/` is supported. Uploading only the notebook downloads the small data file directly from UCI and verifies the checksum. That fallback requires internet access; it fails clearly rather than substituting data.

The notebook writes summary CSVs and a PNG to `outputs/01_human_biology/` relative to the notebook's working directory. Source readings and data retrieval verified on October 13, 2026.
