# Use the two final labs on CloudBank

Keep the existing classroom folders and the paths in the supplied notebooks. The screenshot shows the two science labs alongside `microscopy/`, `oceanography/`, and `workshop_data/`. The Airbnb and GPU rubric notebooks are separate class materials; they are excluded from this repository.

The repository retains its existing filenames: `notebooks/03_microscopy.ipynb` is presentation lab **LEC-2**, and `notebooks/02_oceanography.ipynb` is **LEC-3**. Their contents are byte-for-byte copies of the supplied final files. Use your existing CloudBank notebook names when replacing classroom copies.

## Packages

If your classroom permits conda environments, create and register the environment from the repository root in the JupyterLab terminal:

```bash
conda env create -f environment.yml
conda activate lec2026-ai
python -m ipykernel install --user --name lec2026-ai --display-name "Python (LEC2026 AI)"
```

Refresh the existing CloudBank page and select **Python (LEC2026 AI)**. Continue using the classroom’s Jupyter server. If the classroom uses a fixed environment, its administrator can install the packages listed in `environment.yml` instead.

Both labs need NumPy, pandas, matplotlib, IPython, and ipywidgets. Microscopy also needs SciPy and scikit-image, plus requests for its fallback image download. They run on CPU without an AI API key. The supplied CloudBank notebooks record Python 3.13.14; the optional conda environment targets Python 3.11 rather than claiming to reproduce the classroom image exactly.

The microscopy notebook retains its unconditional `!pip install -qqq scikit-image` setup command. The oceanography notebook reports missing packages and leaves `INSTALL_MISSING = False`. Prepare the kernel before the session. Each lab provides a direct function call if widgets do not display; the live controls have not been independently retested here.

## Existing data paths

Paths below are relative to the kernel’s working directory, which need not match the location shown in the file browser.

**Microscopy:** searches the working directory, its parent, and its `workshop/` child for `microscopy/mitosis.tif`. The selected folder is `ROOT`. If no file is found, it downloads the verified image to `microscopy/mitosis.tif` under the working directory. The notebook verifies the image hash, shape, and type.

**Oceanography:** searches, in order:

1. `../oceanography/p02w_upper600_erddap.csv`
2. `oceanography/p02w_upper600_erddap.csv`
3. `p02w_upper600_erddap.csv` in the working directory

If absent, it downloads to `workshop_data/oceanography/p02w_upper600_erddap.csv`. A hash comparison reports whether the CSV matches the teaching snapshot; a fresh source download may differ.

No dataset files are included in the current Git tree. Use the already prepared classroom files or the existing notebook download fallbacks; no path edits or data moves are required.

## Export paths

The final notebooks retain their supplied export expressions:

- Microscopy: `ROOT / "../results/microscopy"`.
- Oceanography, when `DATA_PATH.parent.name == "oceanography"`: `DATA_PATH.parent.parent.parent / "results/oceanography"`.
- Oceanography otherwise: `Path.cwd() / "workshop_outputs/oceanography"`.

In the supplied saved CloudBank runs, these resolved to `/home/jovyan/results/microscopy` and `/home/jovyan/results/oceanography`. They can sit outside the visible shared folder. Read the notebook’s printed save location; do not assume the exports are beside the notebooks. These expressions have been preserved unchanged.

Run cells in order when you test the classroom copies. The two PDF lab reports explain the methods and saved results; checking those saved results does not replace a fresh classroom run.
