"""Build the microscopy and Hugging Face teaching notebooks."""
from pathlib import Path
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]

def markdown(s):
    return {"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(s).strip() + "\n"}

def code(s):
    return {"cell_type": "code", "metadata": {}, "source": textwrap.dedent(s).strip() + "\n", "execution_count": None, "outputs": []}

def save(name, cells):
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"}}, "cells": cells}
    for i, cell in enumerate(cells):
        cell["id"] = f"{name[:2]}-cell-{i:02d}"
    (ROOT / "notebooks" / name).write_text(json.dumps(notebook, indent=1), encoding="utf-8")

save("03_microscopy.ipynb", [
markdown('''
    # Microscopy: from pixels to measurements
    **Faculty AI workshop · CloudBank Classroom · CPU · 10-minute instructor demo**

    Use a real fluorescence microscopy field to build an adjustable segmentation tool.
    Participants predict what will happen before the instructor moves a slider. You can
    run the prepared code without writing Python; each cell does one job.

    **Questions:** How does a threshold change the objects we measure? When does one
    bright region become several objects? Which measurements need calibration or human checking?

    **Data:** scikit-image `human_mitosis`, 512 × 512 grayscale image, copyright David Root,
    CC0. This is one field of human cells imaged during the work of Moffat et al. (2006).
    The image has no supplied pixel-size calibration or reference segmentation in this kit.
    We therefore report area in pixels², not µm², and call the output **segmented objects**.
    Counting these objects does not establish the number of cells or the mitotic index.

    [Data documentation and attribution](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.human_mitosis)
    · [Licensing discussion](https://github.com/CellProfiler/examples/issues/41)
    · [Source paper](https://doi.org/10.1016/j.cell.2006.01.040)
'''),
markdown('''
    ## 1. Open and check the environment
    In CloudBank Classroom, open this notebook from the distributed `workshop/notebooks`
    folder, choose a Python kernel, and run cells in order with **Shift+Enter**.
    The instructor should prepare dependencies before the workshop. If any are missing,
    use the optional installation line below only if your classroom permits package installs;
    restart the kernel after installation. No GPU, model, account token, or remote inference is used here.
'''),
code('''
    import importlib.util, sys
    modules = ["numpy", "pandas", "matplotlib", "scipy", "skimage", "ipywidgets"]
    missing = [m for m in modules if importlib.util.find_spec(m) is None]
    print("Python:", sys.version.split()[0], "| Missing packages:", missing or "none")
    # Optional instructor setup (uncomment only if needed):
    # %pip install numpy pandas matplotlib scipy scikit-image ipywidgets
    if missing:
        raise ImportError("Install the missing packages using the classroom setup guide, then restart.")
'''),
code('''
    from pathlib import Path
    import hashlib
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import ndimage as ndi
    from skimage import io, filters, morphology, measure, segmentation, feature, color
    from IPython.display import display
    import ipywidgets as widgets
    plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False})

    roots = [Path.cwd(), Path.cwd().parent, Path.cwd() / "workshop"]
    ROOT = next((p for p in roots if (p / "data/microscopy/mitosis.tif").exists()), Path.cwd())
    IMAGE_PATH = ROOT / "data/microscopy/mitosis.tif"
    EXPECTED_SHA256 = "2751ba667c4067c5d30817cff004aa06f6f6287f1cdbb5b8c9c6a500308cb456"
    SOURCE_URL = "https://gitlab.com/scikit-image/data/-/raw/2cdc5ce89b334d28f06a58c9f0ca21aa6992a5ba/AS_09125_050116030001_D03f00d0.tif"
    if not IMAGE_PATH.exists():
        # Standalone notebook fallback; bundled data is preferred during class.
        import requests
        response = requests.get(SOURCE_URL, timeout=60)
        response.raise_for_status()
        if hashlib.sha256(response.content).hexdigest() != EXPECTED_SHA256:
            raise ValueError("Downloaded image differs from the verified teaching image.")
        IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        IMAGE_PATH.write_bytes(response.content)
    assert hashlib.sha256(IMAGE_PATH.read_bytes()).hexdigest() == EXPECTED_SHA256
    image = io.imread(IMAGE_PATH)
    assert image.shape == (512, 512) and image.dtype == np.uint8
    print(f"Loaded {image.shape} grayscale pixels, intensity range {image.min()}–{image.max()}")
'''),
markdown('''
    ## 2. Inspect before measuring
    Bright stain can form touching regions, fragments, or several structures belonging to
    one biological cell. Image intensity is an uncalibrated 8-bit value (0–255); it is not
    a count of molecules. Discuss which structures should count as one object before
    evaluating a segmentation.
'''),
code('''
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(image, cmap="gray", vmin=0, vmax=255)
    axes[0].set(title="Original field", xlabel="x (pixels)", ylabel="y (pixels)")
    axes[1].hist(image.ravel(), bins=64, color="#216869")
    axes[1].set(title="Intensity distribution", xlabel="Intensity (0–255)", ylabel="Number of pixels", yscale="log")
    fig.tight_layout()
    plt.show()
'''),
markdown('''
    ## 3. Build a transparent measurement function
    1. Smooth small intensity fluctuations with a Gaussian filter.
    2. Start from an Otsu intensity threshold; multiply it by a user-selected factor.
    3. Remove very small regions and fill small holes.
    4. Find separated peaks in a distance transform, then use watershed to split touching regions.
    5. Measure regions and flag those touching an image edge.

    A larger threshold keeps fewer bright pixels; a larger seed spacing usually makes
    fewer watershed seeds. These controls change the assumptions behind the measurements.
'''),
code('''
    def segment_and_measure(threshold_factor=1.0, min_area=40, seed_spacing=8, exclude_edges=False):
        smoothed = filters.gaussian(image, sigma=1.0, preserve_range=True)
        threshold = float(filters.threshold_otsu(smoothed)) * float(threshold_factor)
        mask = smoothed > threshold
        # Connected components here are explicit, avoiding version-specific bool cleanup APIs.
        connected = measure.label(mask)
        sizes = np.bincount(connected.ravel())
        keep = sizes >= int(min_area)
        keep[0] = False
        mask = ndi.binary_fill_holes(keep[connected])
        distance = ndi.distance_transform_edt(mask)
        peaks = feature.peak_local_max(distance, min_distance=int(seed_spacing), labels=mask, exclude_border=False)
        markers = np.zeros(image.shape, dtype=np.int32)
        if len(peaks):
            markers[tuple(peaks.T)] = np.arange(1, len(peaks) + 1)
        labels = segmentation.watershed(-distance, markers, mask=mask)
        if exclude_edges:
            labels = segmentation.clear_border(labels)
        # Splitting can introduce small segments; apply the same minimum area after splitting.
        sizes = np.bincount(labels.ravel())
        keep = sizes >= int(min_area)
        keep[0] = False
        labels[~keep[labels]] = 0
        labels, _, _ = segmentation.relabel_sequential(labels)
        records = []
        for region in measure.regionprops(labels, intensity_image=image):
            r0, c0, r1, c1 = region.bbox
            records.append({"object_id": region.label, "area_px2": region.area,
                            "mean_intensity_0_255": region.mean_intensity,
                            "centroid_y_px": region.centroid[0], "centroid_x_px": region.centroid[1],
                            "touches_edge": r0 == 0 or c0 == 0 or r1 == image.shape[0] or c1 == image.shape[1]})
        columns = ["object_id", "area_px2", "mean_intensity_0_255", "centroid_y_px", "centroid_x_px", "touches_edge"]
        table = pd.DataFrame(records, columns=columns)
        return labels, table, threshold

    labels, objects, threshold = segment_and_measure()
    print(f"Threshold {threshold:.1f}; {len(objects)} segmented objects; {int(objects.touches_edge.sum())} touch an edge")
    display(objects.head())
'''),
code('''
    def show_segmentation(threshold_factor=1.0, min_area=40, seed_spacing=8, exclude_edges=False):
        labels, table, threshold = segment_and_measure(threshold_factor, min_area, seed_spacing, exclude_edges)
        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        axes[0].imshow(image, cmap="gray", vmin=0, vmax=255)
        axes[0].set(title="Source image")
        axes[1].imshow(color.label2rgb(labels, image=image, bg_label=0, alpha=0.35))
        axes[1].set(title=f"{len(table)} objects · threshold {threshold:.1f}")
        for ax in axes[:2]:
            ax.set(xlabel="x (pixels)", ylabel="y (pixels)")
        axes[2].hist(table.area_px2, bins=25, color="#216869")
        axes[2].set(title="Measured object sizes", xlabel="Area (pixels²)", ylabel="Number of objects")
        fig.tight_layout()
        plt.show()
        print("Edge-touching objects:", int(table.touches_edge.sum()), "| These are algorithm outputs, not verified cells.")
    show_segmentation()
'''),
markdown('''
    ## 4. Use the tool without editing code
    **Predict → change one control → inspect the overlay → explain the difference.**
    If sliders do not render in the classroom interface, use the one-line function call
    in the next cell. Function inputs and widget inputs perform the same analysis.
'''),
code('''
    controls = {
        "threshold_factor": widgets.FloatSlider(value=1.0, min=0.65, max=1.5, step=0.05, description="Threshold", continuous_update=False),
        "min_area": widgets.IntSlider(value=40, min=10, max=200, step=10, description="Min area", continuous_update=False),
        "seed_spacing": widgets.IntSlider(value=8, min=3, max=20, step=1, description="Seed gap", continuous_update=False),
        "exclude_edges": widgets.Checkbox(value=False, description="Exclude edges")}
    output = widgets.interactive_output(show_segmentation, controls)
    display(widgets.VBox(list(controls.values())), output)
'''),
code('''
    # A portable fallback if widget controls are unavailable.
    show_segmentation(threshold_factor=1.1, min_area=40, seed_spacing=8, exclude_edges=False)
'''),
markdown('''
    ## 5. Check sensitivity instead of trusting one result
    There is no reference mask here, so this table measures **sensitivity**, not accuracy.
    A stable result can still be wrong. Regions in the same field are not independent
    biological replicates; do not turn this table into a treatment-comparison significance test.
'''),
code('''
    rows = []
    for factor in [0.8, 1.0, 1.2]:
        for spacing in [5, 8, 12]:
            lbl, tbl, cutoff = segment_and_measure(factor, 40, spacing)
            rows.append({"threshold_factor": factor, "seed_spacing_px": spacing,
                         "n_objects": len(tbl), "median_area_px2": tbl.area_px2.median(),
                         "foreground_percent": 100 * np.mean(lbl > 0)})
    sensitivity = pd.DataFrame(rows)
    display(sensitivity.round(2))
    matrix = sensitivity.pivot(index="threshold_factor", columns="seed_spacing_px", values="n_objects")
    fig, ax = plt.subplots(figsize=(5, 3))
    im = ax.imshow(matrix.to_numpy(), cmap="viridis", aspect="auto")
    ax.set(xticks=range(3), xticklabels=matrix.columns, yticks=range(3), yticklabels=matrix.index,
           xlabel="Seed spacing (pixels)", ylabel="Threshold factor", title="Object count changes with assumptions")
    for row in range(3):
        for col in range(3):
            ax.text(col, row, str(matrix.iloc[row, col]), ha="center", va="center", color="white")
    fig.colorbar(im, ax=ax, label="Segmented object count")
    fig.tight_layout()
    plt.show()
'''),
markdown('''
    ## 6. Inspect a small area by eye
    Mark one plausible biological structure and compare it with the overlay. Is it missed,
    split, or merged? Define the intended objects first. Have two people independently
    annotate the same crop, then discuss disagreement before adopting a reference mask.
'''),
code('''
    labels, objects, threshold = segment_and_measure()
    crop = (slice(128, 256), slice(128, 256))
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    axes[0].imshow(image[crop], cmap="gray")
    axes[1].imshow(color.label2rgb(labels[crop], image=image[crop], bg_label=0, alpha=0.4))
    axes[0].set_title("Inspect this crop by eye")
    axes[1].set_title("Compare with the segmentation")
    for ax in axes:
        ax.set(xlabel="Crop x (pixels)", ylabel="Crop y (pixels)")
    fig.tight_layout()
    plt.show()
'''),
markdown('''
    ## 7. Ask AI to modify the tool
    Copy a prompt to your approved AI assistant and give it the function above:

    > Modify `show_segmentation` to add a checkbox that highlights objects touching the
    > image border. Keep the source image, segmentation method, pixel units, and other
    > controls unchanged. Return one replacement code cell and explain how I can check it.

    Verify the modification on the crop. Then try:

    > Add a size filter to the measurement table. Show the number of objects removed.
    > Do not describe remaining objects as verified cells or convert pixels² to µm².

    **Debrief:** Which choices belong to the scientist? Which can AI implement? What
    evidence would be needed to call these outputs accurate cell counts?
'''),
markdown('''
    ## 8. Export a reproducible result
    This cell exports the **default** settings, independent of the last slider position.
    Edit the settings here if you want to save another analysis. The settings JSON records
    parameters and the image hash, so the table has a traceable source.
'''),
code('''
    import json, importlib.metadata as metadata
    settings = {"threshold_factor": 1.0, "min_area": 40, "seed_spacing": 8, "exclude_edges": False}
    labels, objects, threshold = segment_and_measure(**settings)
    result_dir = ROOT / "results/microscopy"
    result_dir.mkdir(parents=True, exist_ok=True)
    objects.to_csv(result_dir / "objects.csv", index=False)
    io.imsave(result_dir / "segmentation.tif", labels.astype(np.uint16), check_contrast=False)
    record = {"source_url": SOURCE_URL, "image_sha256": EXPECTED_SHA256,
              "parameters": settings, "intensity_threshold": threshold,
              "software": {p: metadata.version(p) for p in ["numpy", "scipy", "scikit-image", "pandas"]},
              "interpretation": "Unvalidated segmented objects from one microscopy field; pixel units."}
    (result_dir / "settings.json").write_text(json.dumps(record, indent=2))
    print("Saved results to", result_dir)
'''),
markdown('''
    ## More candidate datasets
    - **BloodMNIST:** 17,092 resized blood-cell images in eight classes; CC BY 4.0.
      Good for a later classification exercise. Download through the official MedMNIST
      Zenodo record, and preserve its train/validation/test split. Resizing loses morphology.
      [Official project](https://medmnist.com/) · [Official data](https://zenodo.org/records/10519652)
    - **Quantitative phase cell (`skimage.data.cell`):** one CC0 cell image with 0.107 µm
      pixel spacing. A good follow-up for converting area from pixels² to µm² and discussing
      background banding. [Documentation](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell)
''')])

save("04_huggingface_tools.ipynb", [
markdown('''
    # Hugging Face: use an existing model as a tool
    **Faculty AI workshop · CloudBank Classroom · CPU · optional third-part demo (15 minutes)**

    Run a small pretrained sentiment classifier, then call a public Gradio app as a remote
    tool. This connects the short-text activity to reusable models and APIs.

    **Questions:** Does a sentiment model implement our extraction rubric? What happens
    to neutral or mixed text when the model has only two labels? Where does computation happen?

    The prepared model uses approximately 268 MB of weights. Pre-download it before class
    and allow additional memory for PyTorch. A CPU is sufficient; use the three scientific
    notebooks if this environment cannot fit or download it. Public Hub model downloads
    need no API token. These demos do not invoke paid inference providers.
'''),
markdown('''
    ## 1. Instructor dependency check
    Use a Python 3.10+ kernel. Install dependencies before class if your classroom permits it,
    then restart the kernel. The scientific notebooks do not need these extra dependencies.
'''),
code('''
    import sys, importlib.util
    packages = ["torch", "transformers", "pandas", "huggingface_hub", "gradio_client", "ipywidgets"]
    missing = [p for p in packages if importlib.util.find_spec(p) is None]
    print("Python:", sys.version.split()[0], "| Missing packages:", missing or "none")
    # Optional instructor setup (uncomment if needed):
    # %pip install 'transformers>=4.45,<5' torch pandas huggingface-hub gradio-client
    if missing:
        raise ImportError("Prepare the Hugging Face dependencies before running this demo.")
'''),
markdown('''
    ## 2. Read the model card before running it
    We use `distilbert/distilbert-base-uncased-finetuned-sst-2-english` (Apache 2.0).
    It was fine-tuned on English movie-review sentiment (SST-2). It has **POSITIVE** and
    **NEGATIVE** labels; it cannot return neutral or mixed, extract adverse effects, or
    judge the truth of a health statement. A high softmax score is not a calibrated
    probability of correctness on our workshop data.

    [Model card](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english)
    · [Transformers pipelines documentation](https://huggingface.co/docs/transformers/main_classes/pipelines)
'''),
code('''
    from pathlib import Path
    import os
    import pandas as pd
    from IPython.display import display
    roots = [Path.cwd(), Path.cwd().parent, Path.cwd() / "workshop"]
    ROOT = next((p for p in roots if (p / "notebooks").is_dir()), Path.cwd())
    # Save the cache inside the workshop folder so your classroom copy can reuse it.
    os.environ.setdefault("HF_HOME", str(ROOT / ".cache/huggingface"))
    MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    REVISION = "714eb0fa89d2f80546fda750413ed43d93601a13"  # verified Hub commit
    from transformers import pipeline
    sentiment = pipeline("sentiment-analysis", model=MODEL_ID, revision=REVISION,
                         device=-1, trust_remote_code=False, model_kwargs={"use_safetensors": True})
    print("Loaded", MODEL_ID, "revision", REVISION, "on CPU")
'''),
markdown('''
    ## 3. Run a model; inspect its output
    The six sentences below are **instructor-authored teaching examples**, not dataset
    records. Human labels follow the four-category workshop rubric and include mixed and
    neutral examples to expose the model's two-label constraint.
'''),
code('''
    examples = pd.DataFrame([
        {"text": "The food was delicious and the staff were wonderful.", "human_rubric": "positive"},
        {"text": "The product broke immediately and the support was terrible.", "human_rubric": "negative"},
        {"text": "The package arrived on Tuesday.", "human_rubric": "neutral"},
        {"text": "The screen is excellent, but the battery is terrible.", "human_rubric": "mixed"},
        {"text": "I expected to hate this film, but I loved it.", "human_rubric": "positive"},
        {"text": "The story was neither good nor bad.", "human_rubric": "neutral"},
    ])
    predictions = sentiment(examples.text.tolist(), truncation=True, max_length=512, batch_size=4)
    examples["model_label"] = [p["label"].lower() for p in predictions]
    examples["model_score"] = [p["score"] for p in predictions]
    examples["rubric_has_label_model_cannot_return"] = examples.human_rubric.isin(["neutral", "mixed"])
    display(examples)
    print("Discuss disagreements; six selected examples are not a model accuracy benchmark.")
'''),
markdown('''
    ## 4. Wrap it in an analysis tool
    A tool is a callable function with inputs and outputs. The same function can be
    reused from a notebook, connected to an app, or offered to an AI agent. Here a
    text box is sufficient; no agent orchestration is needed to demonstrate the idea.
'''),
code('''
    def classify_review(text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Enter a nonempty review.")
        pred = sentiment(text, truncation=True, max_length=512)[0]
        return {"text": text, "label": pred["label"].lower(), "score": round(pred["score"], 4),
                "model": MODEL_ID, "revision": REVISION,
                "note": "Binary sentiment only; inputs longer than 512 tokens are truncated."}

    display(classify_review("The seminar was useful, but the room was uncomfortable."))
'''),
code('''
    # The notebook's text-box tool. The function call above works if widgets are unavailable.
    import ipywidgets as widgets
    text_box = widgets.Textarea(value="The seminar was useful, but the room was uncomfortable.",
                               description="Review:", layout=widgets.Layout(width="85%"))
    button = widgets.Button(description="Classify locally", button_style="info")
    output = widgets.Output()
    def run_review(_):
        with output:
            output.clear_output(wait=True)
            display(classify_review(text_box.value))
    button.on_click(run_review)
    display(text_box, button, output)
'''),
markdown('''
    ## 5. Compare with the real reviews from Part 1 (optional)
    Use the bundled UCI review sentences as a bridge to the earlier prompt activity.
    Their original annotation is binary sentiment, so it is compatible with this model's
    label set. A workshop convenience sample still does not establish general performance.
    Inspect the actual JSONL file and choose the text/label fields in the next cell.
'''),
code('''
    import json
    review_path = ROOT / "part1/data/reviews.jsonl"
    if review_path.exists():
        records = [json.loads(line) for line in review_path.read_text().splitlines() if line.strip()]
        review_texts = [r["text"] for r in records[:10]]
        results = sentiment(review_texts, truncation=True, max_length=512, batch_size=4)
        display(pd.DataFrame({"text": review_texts,
                              "model_label": [r["label"] for r in results],
                              "model_score": [r["score"] for r in results]}))
    else:
        print("Optional: distribute the full workshop folder to use the Part 1 review sample.")
'''),
markdown('''
    ## 6. Call an existing tool hosted on Hugging Face Spaces
    **Models** contain downloadable trained weights. **Spaces** host apps; a Gradio app
    can expose callable endpoints. The call below performs computation on a remote Space.
    We send only the literal numbers 4 and 5 to the official Gradio calculator example.
    Review the input policy before sending your own course data to a remote service.

    Set `RUN_REMOTE_SPACE = True` to connect. Public Spaces can sleep, change their API,
    queue requests, or be unavailable; the scientific notebooks remain usable offline.
    `view_api()` shows the current signature rather than guessing argument names.

    [Space](https://huggingface.co/spaces/gradio/calculator)
    · [Official Python client guide](https://gradio.app/guides/getting-started-with-the-python-client)
'''),
code('''
    RUN_REMOTE_SPACE = False  # instructor opt-in: the next cell sends a remote request
    if RUN_REMOTE_SPACE:
        from gradio_client import Client
        client = Client("gradio/calculator", httpx_kwargs={"timeout": 30.0})
        client.view_api()
    else:
        print("Remote Space call off. Set RUN_REMOTE_SPACE=True to inspect its API.")
'''),
code('''
    if RUN_REMOTE_SPACE:
        # Signature documented by Gradio; inspect view_api above in case the Space changed.
        job = client.submit(num1=4, operation="add", num2=5, api_name="/predict")
        try:
            print("Remote calculator result:", job.result(timeout=30))
        except TimeoutError:
            job.cancel()
            print("The public Space did not respond within 30 seconds; use the local model demo.")
'''),
markdown('''
    ## 7. Teaching prompts and next steps
    > Explain `pipeline` and `classify_review` for a faculty member who has never used
    > Python. Identify what is downloaded, where the prediction runs, what is sent to a
    > remote service, and which rubric categories the model cannot return.

    > Using the existing classifier, create a table that groups review predictions by
    > label and counts them. Preserve the source text and model revision. Do not describe
    > the score as accuracy, and do not convert the binary model into a four-category classifier.

    **Extension:** Choose a domain-specific model or Space from Hugging Face. Inspect
    its card, license, task, input format, output labels, hardware needs, and evaluation
    domain. For microscopy, a segmentation model must be compared with reference masks
    from an appropriate modality. A general image classifier is not a cell-counting tool.
    For ocean profiles, deterministic analysis often answers the teaching question directly;
    an LLM can help implement and explain the tool without replacing the measurement.

    **Exit ticket:** Name one useful AI interaction, one validation you would require,
    and one change you would make before using this exercise in your course.
''')])
