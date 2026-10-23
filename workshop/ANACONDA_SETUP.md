# Anaconda environment for the workshop

The repository's [environment.yml](../environment.yml) creates **lec2026-ai**, a Python 3.11 environment for all four notebooks. It includes scientific analysis/image-processing packages, JupyterLab and widgets, Hugging Face dependencies, and packages used by the supplied notebook authoring/execution utilities.

## 1. Install Anaconda

If Anaconda is not installed, follow the [official installation instructions](https://www.anaconda.com/docs/getting-started/anaconda/install) for your operating system. Open **Anaconda Prompt** on Windows, or a terminal configured for conda on macOS/Linux. Confirm conda is available:

```bash
conda --version
```

## 2. Create and activate the environment

Change to the repository's root folder, `LEC2026`, where `environment.yml` is located. Run these commands once:

```bash
conda env create -f environment.yml
conda activate lec2026-ai
```

The YAML file uses conda-forge for Python, Jupyter, and scientific packages, then installs the Hugging Face packages with pip inside that environment. Conda handles both steps. The version ranges match the existing workshop requirements files; this is an environment specification rather than a platform-specific lockfile. [Conda environment documentation](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html).

## 3. Register the notebook kernel

With `lec2026-ai` active, register it with Jupyter:

```bash
python -m ipykernel install --user --name lec2026-ai --display-name "Python (LEC2026 AI)"
```

This makes the environment available by name in the Jupyter kernel menu, including when the Jupyter server runs in another environment. [IPython kernel registration instructions](https://ipython.readthedocs.io/en/stable/install/kernel_install.html).

## 4. Open the notebooks

From the repository root:

```bash
jupyter lab workshop/notebooks
```

Open a notebook, choose **Kernel → Change Kernel → Python (LEC2026 AI)**, then run cells in order. A terminal session started later needs only:

```bash
conda activate lec2026-ai
jupyter lab workshop/notebooks
```

The same environment covers:

| Notebook or tool | Main dependencies |
|---|---|
| Human biology | NumPy, pandas, matplotlib, ipywidgets |
| Oceanography | NumPy, pandas, matplotlib, ipywidgets |
| Microscopy | NumPy, pandas, matplotlib, SciPy, scikit-image, requests, ipywidgets |
| Hugging Face tools | PyTorch, Transformers, huggingface-hub, gradio-client, pandas, ipywidgets |
| Notebook interface and authoring utilities | JupyterLab, IPython, ipykernel, jupyterlab_widgets, nbformat, nbclient, jupyter_client |

All notebook demos use CPU. The Hugging Face notebook downloads its model weights on first use; environment creation installs software without downloading the workshop datasets or model weights. Its optional remote Space call remains off by default. Langflow/Dify setup for the separate no-code app demo is described in the [Part 1 guide](part1/GUIDE.md).

## CloudBank Classroom

If conda environments are supported in your classroom image, run steps 2 and 3 in the **JupyterLab terminal**, starting from the uploaded/cloned repository root. Refresh the existing CloudBank JupyterLab page and choose **Python (LEC2026 AI)** for each notebook. Continue using the classroom's existing Jupyter server.

If the new kernel is absent, ask the classroom administrator to expose that kernel or build the environment into the course image. For classroom images that use a preconfigured Python environment instead of conda, follow [CLOUDBANK_SETUP.md](CLOUDBANK_SETUP.md).

## Update an existing environment

When `environment.yml` changes, update the environment from the repository root, then restart the notebook kernel:

```bash
conda env update --name lec2026-ai --file environment.yml
conda activate lec2026-ai
```

Keep workshop-specific package changes in `environment.yml` so the environment can be recreated. The complete environment has not been installed or tested as part of this documentation change, in keeping with your request to test later.

## Common setup issues

- **`conda` is not recognized:** open Anaconda Prompt on Windows; on macOS/Linux, follow Anaconda's shell setup instructions and reopen the terminal.
- **Environment already exists:** use the update command above instead of creating it again.
- **A notebook says a package is missing:** check that its selected kernel is **Python (LEC2026 AI)**. Installing a package into `base` or another environment will not make it available in this kernel.
- **Widgets show as text:** confirm the kernel selection and refresh JupyterLab. On a managed JupyterHub, widget support may also need to be enabled in the server environment by the administrator. The scientific notebooks include direct function-call alternatives.
- **PyTorch installation fails for your platform:** use the [official PyTorch installation selector](https://docs.pytorch.org/get-started/locally/) to select a supported build inside `lec2026-ai`. The notebooks do not require CUDA.
