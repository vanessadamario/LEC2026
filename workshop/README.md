# AI interaction for faculty

**90 minutes · CloudBank Classroom · beginner faculty · CPU notebooks**

Start with [SESSION_GUIDE.md](SESSION_GUIDE.md) for the agenda, dataset choices, teaching questions, and demo script. [Part 1 guide](part1/GUIDE.md) contains the text extraction activity, predefined rubrics, copy-paste prompts, and Langflow workflow.

## Notebooks

1. [Human biology](notebooks/01_human_biology.ipynb): numeric measurements, missingness, uncertainty, age stratification, and an interactive scatterplot tool.
2. [Oceanography](notebooks/02_oceanography.ipynb): temperature/salinity profiles, source quality flags, unequal coverage, and an interactive profile viewer.
3. [Microscopy](notebooks/03_microscopy.ipynb): thresholding, watershed, region measurements, and an interactive segmentation tool.
4. [Hugging Face tools](notebooks/04_huggingface_tools.ipynb): a pretrained sentiment model running on the notebook CPU, plus an opt-in remote Gradio Space call.

The three science notebooks use bundled real data. Keep the folder structure when distributing the materials. Their analyses do not require an AI API key or GPU. The optional Hugging Face notebook downloads model weights on its first run unless the classroom cache is prepared; its remote Space call is disabled by default.

## CloudBank delivery

Upload and extract the complete workshop ZIP into participants' persistent JupyterHub storage, or distribute the folder through your established classroom repository/nbgitpuller workflow. Open `workshop/notebooks/` and select a Python 3.10+ kernel. CloudBank Classroom is a JupyterHub service; your specific environment and allocation determine available packages and resources. [CloudBank's official guide](https://www.cloudbank.org/training/access-cloudbank-classroom).

For instructor preparation, use [CLOUDBANK_SETUP.md](CLOUDBANK_SETUP.md). Dependency manifests are [requirements-core.txt](requirements-core.txt) and [requirements-huggingface.txt](requirements-huggingface.txt).

## Creation and execution status

Materials are created. Source access and dataset licenses were checked. Some human-biology and oceanography code was run during preparation before the request to defer testing. Further execution stopped at that request. The complete notebook suite, microscopy notebook, Hugging Face model/Space calls, and actual CloudBank browser controls have **not** been validated end to end. Test them later in your classroom environment as requested; no model outputs are fabricated.

The session guide includes a slide outline and a concrete Langflow recipe you can use to prepare the presentation and app demonstration.
