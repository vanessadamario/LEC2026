# **From AI Idea to AI Infrastructure**

90-minute LEC 2026 faculty session, following the presentation from AI ideas and NAIRR resources to no-code workflows, CloudBank notebooks, and a project plan.

## **1. Start with the idea**

Define your teaching or research question, the data you need, and how you will check the result before choosing a model or computing resource.

Resources discussed in the slides: [NAIRR Pilot](https://nairrpilot.org), [ACCESS recorded events and training](https://support.access-ci.org/knowledge-base/recorded-events-and-trainings), and [NRP LLM status](https://nrp.ai/llm-status/).

## **2. No-code: compare models and extract structured information**

Use the same image and rubric across models, then inspect the evidence behind each answer. The [visual-framing prompt](workshop/part1/prompts/visual_framing.md) supports the presentation’s image-analysis example in Langflow. It turns visible cues into a JSON record; human review checks whether those cues support the assigned fields.

The draft slides remain local until they are ready to publish.

## **3. Basic coding: explore and modify a disciplinary tool**

The two supplied final notebooks are included unchanged, with their saved outputs. Repository filenames and every data/output path inside them are preserved. Lab numbers below follow the presentation.

| Lab | Notebook | Detailed explanation |
|---|---|---|
| LEC-2 · Microscopy: automated segmentation | [Open notebook](workshop/notebooks/03_microscopy.ipynb) | [Illustrated lab PDF](workshop/reports/microscopy_analysis_report.pdf) |
| LEC-3 · Oceanography: automated analysis | [Open notebook](workshop/notebooks/02_oceanography.ipynb) | [Dataset and analysis PDF](workshop/reports/oceanography_dataset_report.pdf) |

Predict a change, adjust one control, inspect the result, and explain what changed. Then ask an AI assistant for one small modification and check it against the original analysis.

The Airbnb lab and separate GPU rubric notebook shown in the classroom screenshot are existing class materials and are not included here.

### **Run on CloudBank**

Use your existing classroom environment and folder layout. [CloudBank instructions](workshop/CLOUDBANK_SETUP.md) describe the exact supplied paths, package setup, and export locations. Do not move the classroom data folders to match older workshop drafts.

### **Run with Anaconda**

From this repository’s root, in Anaconda Prompt or a conda-enabled terminal:

```bash
conda env create -f environment.yml
conda activate lec2026-ai
python -m ipykernel install --user --name lec2026-ai --display-name "Python (LEC2026 AI)"
jupyter lab workshop/notebooks
```

Choose **Python (LEC2026 AI)** as the notebook kernel. Both labs run on CPU. This environment includes the dependencies for these two labs; it does not install a no-code service or an AI model.

To update an existing environment:

```bash
conda env update --name lec2026-ai --file environment.yml
```

The notebooks download their source data if no recognized local file is present. A first download needs internet access; prepared local data supports offline use. The microscopy setup cell retains the supplied `!pip install -qqq scikit-image` command.

## **4. Turn your idea into a next step**

Write down your goal, input data, proposed tool, validation method, compute/access needs, and next action. Use those details to plan a classroom adaptation or a resource request.
