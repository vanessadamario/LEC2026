# LEC2026: AI interaction for faculty

A 90-minute workshop with short-text prompt engineering, three scientific analysis notebooks, and a Hugging Face tools demonstration. See the [workshop guide](workshop/SESSION_GUIDE.md) for the agenda and [materials index](workshop/README.md) for the notebooks and prompts.

## Create the Anaconda environment

With Anaconda installed, open Anaconda Prompt on Windows or a conda-enabled terminal on macOS/Linux. Change to this repository's root folder, then run:

```bash
conda env create -f environment.yml
conda activate lec2026-ai
python -m ipykernel install --user --name lec2026-ai --display-name "Python (LEC2026 AI)"
jupyter lab workshop/notebooks
```

In JupyterLab, open a notebook and choose **Python (LEC2026 AI)** as its kernel. The [environment file](environment.yml) includes Python 3.11, JupyterLab, interactive widgets, all scientific notebook dependencies, and the Hugging Face model/client dependencies. The notebooks run on CPU.

For installation, CloudBank Classroom use, updating the environment, and troubleshooting, see [Anaconda setup instructions](workshop/ANACONDA_SETUP.md). These commands are setup instructions; environment installation and notebook testing are left for you to run later.

## Data

Dataset files, downloaded model caches, generated outputs, and the data-containing workshop ZIP are excluded by [.gitignore](.gitignore). Source/license notes and download metadata remain with the materials. The scientific notebooks have source-download fallbacks when their local data files are absent; the Part 1 text activity uses separate source snapshots described in its [guide](workshop/part1/GUIDE.md).

Ignore rules do not remove datasets from earlier Git commits. Existing history must be cleaned separately before publishing a repository that excludes those datasets throughout its history.
