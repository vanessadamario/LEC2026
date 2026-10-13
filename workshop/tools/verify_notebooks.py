"""Execute workshop notebooks and save outputs and representative plot previews."""
from pathlib import Path
import os
import sys
import json
import base64
import time

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
for variable, folder in [("MPLCONFIGDIR", "matplotlib"), ("JUPYTER_CONFIG_DIR", "jupyter/config"),
                         ("JUPYTER_RUNTIME_DIR", "jupyter/runtime"), ("IPYTHONDIR", "ipython"),
                         ("SKIMAGE_DATADIR", "skimage"), ("HF_HOME", "huggingface")]:
    os.environ.setdefault(variable, str(CACHE / folder))
    Path(os.environ[variable]).mkdir(parents=True, exist_ok=True)

import nbformat
from nbclient import NotebookClient

report = []
files = [ROOT / "notebooks" / name for name in sys.argv[1:]] if len(sys.argv) > 1 else sorted((ROOT / "notebooks").glob("*.ipynb"))
for path in files:
    start = time.monotonic()
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=240, kernel_name="python3", resources={"metadata": {"path": str(ROOT / "notebooks")}})
    client.execute()
    nbformat.write(notebook, path)
    pictures = 0
    for index, cell in enumerate(notebook.cells):
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                raise RuntimeError(f"{path.name} cell {index}: {output}")
            data = output.get("data", {})
            if "image/png" in data:
                encoded = data["image/png"]
                if isinstance(encoded, list):
                    encoded = "".join(encoded)
                (ROOT / "previews" / f"{path.stem}_cell{index:02d}_{pictures:02d}.png").write_bytes(base64.b64decode(encoded))
                pictures += 1
    entry = {"notebook": path.name, "cells": len(notebook.cells), "plot_previews": pictures,
             "elapsed_seconds": round(time.monotonic() - start, 2), "status": "passed"}
    report.append(entry)
    print(json.dumps(entry), flush=True)
(ROOT / "notes" / "execution_report.json").write_text(json.dumps(report, indent=2))
