# CloudBank Classroom preparation

Use the existing classroom JupyterHub and the institution's approved AI chat tool. Exact package versions, storage limits, internet access, and memory depend on your classroom configuration; these materials do not change or provision your CloudBank allocation. [Official CloudBank Classroom guide](https://www.cloudbank.org/training/access-cloudbank-classroom).

## Distribute the kit

Upload `faculty_ai_workshop.zip` in JupyterLab and extract it through your normal classroom process. If you need a terminal command, use `unzip faculty_ai_workshop.zip`. The archive contains the top-level `workshop/` folder. Preserve `workshop/data/`, `workshop/part1/`, and `workshop/notebooks/` together. If your classroom already distributes repositories using nbgitpuller, add this folder to that repository through your usual process; this kit has not been published to GitHub.

Choose a Python 3.10+ kernel. The three science demos run on CPU, with small bundled datasets. They can run without source network access once dependencies are installed. Widgets require the classroom notebook interface to support ipywidgets; each science notebook includes a direct function-call fallback.

## Prepare packages before the session

Ask the classroom administrator to include the core packages in the course environment, or, if notebook package installs are permitted, use an instructor setup notebook:

```python
%pip install -r ../requirements-core.txt
```

This relative path assumes the notebook is opened from `workshop/notebooks/`. Restart the kernel after installation. For the optional Hugging Face demo:

```python
%pip install -r ../requirements-huggingface.txt
```

The manifests use version ranges rather than a platform-specific lockfile. They describe intended dependencies; the complete suite has not been tested in your CloudBank image. Each science notebook starts with an environment check. Package installation is disabled/commented by default.

## Prepare the Hugging Face cache later

The Hugging Face notebook pins the model to a verified public Hub commit and requests safetensors weights with remote repository code disabled. Its first model load downloads roughly 268 MB of weights plus small configuration/tokenizer files. Allow disk space and runtime memory beyond that file size for PyTorch and inference. No GPU or paid inference token is required.

When you test later, run the model-load cell in the actual classroom image before the session. The notebook uses `workshop/.cache/huggingface` unless `HF_HOME` is already configured. Distribute a populated cache through your classroom's approved mechanism if desired, retaining the model's Apache 2.0 license; the supplied ZIP does not contain model weights. Avoid simultaneous first downloads by the whole class.

The optional Space section sends a simple numerical calculator request to a public Gradio Space only when `RUN_REMOTE_SPACE = True`. The API can change or the Space can be unavailable. Use the locally running sentiment model for the main demo. In a JupyterHub session, "local" means the classroom server process; it does not mean the participant's laptop.

## Prepare Part 1

Langflow is an instructor demonstration on a preconfigured machine/service; participants need only their approved chat interface and the short-text handouts. Choose the model provider you already have access to and set its credential through the app's credential interface. Keep keys out of notebooks and participant handouts. Langflow itself does not supply unlimited model inference. The kit includes prompts, schemas, import CSVs, and workflow instructions; it does not include an authenticated, deployed flow.

When you rehearse later, start with one record, inspect its JSON against the rubric, then show a small batch and its table export. The bundled validator can check syntax, allowed values, and evidence spans; semantic correctness still needs human comparison with the rubric.
