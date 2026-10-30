"""Extract saved notebook figures and trace intermediate stages for the report.

Does not execute notebook cells, download data, or overwrite notebook exports.
The supplemental trace must match the saved label image before figures are saved.
"""
from pathlib import Path
import os
import json
import hashlib
import base64
import ast
import sys
import importlib.metadata as metadata

REPORTS = Path(__file__).resolve().parent
WORKSHOP = REPORTS.parent
ASSETS = REPORTS / "microscopy_figures"
ASSETS.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/lec2026-microscopy-matplotlib")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import io, filters, measure, segmentation, feature, color

plt.rcParams.update({"font.size": 11, "figure.dpi": 160,
                     "axes.spines.top": False, "axes.spines.right": False})
notebook_path = WORKSHOP / "notebooks/03_microscopy.ipynb"
notebook = json.loads(notebook_path.read_text())
manifest = {"date": "2026-10-24", "notebook_sha256": hashlib.sha256(notebook_path.read_bytes()).hexdigest(),
            "saved_figures": [], "supplemental_figures": [],
            "supplemental_software": {p: metadata.version(p) for p in ["numpy", "scipy", "scikit-image", "pandas", "matplotlib"]}}

names = {5: "01_notebook_intensity.png", 8: "02_notebook_default.png",
         11: "03_notebook_threshold_1p1.png", 13: "04_notebook_sensitivity.png",
         15: "05_notebook_crop.png"}
for cell_index, name in names.items():
    cell = notebook["cells"][cell_index]
    output_index, output = next((j, o) for j, o in enumerate(cell.get("outputs", [])) if "image/png" in o.get("data", {}))
    payload = output["data"]["image/png"]
    if isinstance(payload, list):
        payload = "".join(payload)
    data = base64.b64decode(payload)
    (ASSETS / name).write_bytes(data)
    manifest["saved_figures"].append({"file": name, "cell_index_zero_based": cell_index,
                                       "execution_count": cell.get("execution_count"),
                                       "output_index": output_index, "sha256": hashlib.sha256(data).hexdigest(),
                                       "origin": "Unchanged embedded PNG from the saved notebook"})

image = io.imread(WORKSHOP / "data/microscopy/mitosis.tif")
reference = io.imread(WORKSHOP / "results/microscopy/segmentation.tif")
saved_settings = json.loads((WORKSHOP / "results/microscopy/settings.json").read_text())
manifest["saved_export_software"] = saved_settings["software"]
manifest["image_sha256"] = hashlib.sha256((WORKSHOP / "data/microscopy/mitosis.tif").read_bytes()).hexdigest()
assert manifest["image_sha256"] == saved_settings["image_sha256"]

# Reproduce the operations exactly, retaining arrays the notebook does not plot.
smoothed = filters.gaussian(image, sigma=1.0, preserve_range=True)
otsu = float(filters.threshold_otsu(smoothed))
threshold_mask = smoothed > otsu
connected = measure.label(threshold_mask)
sizes = np.bincount(connected.ravel())
keep = sizes >= 40
keep[0] = False
size_filtered = keep[connected]
filled = ndi.binary_fill_holes(size_filtered)
distance = ndi.distance_transform_edt(filled)
peaks = feature.peak_local_max(distance, min_distance=8, labels=filled, exclude_border=False)
markers = np.zeros(image.shape, dtype=np.int32)
markers[tuple(peaks.T)] = np.arange(1, len(peaks) + 1)
watershed = segmentation.watershed(-distance, markers, mask=filled)
post = watershed.copy()
watershed_sizes = np.bincount(watershed.ravel())
keep_final = watershed_sizes >= 40
keep_final[0] = False
post[~keep_final[post]] = 0
final, _, _ = segmentation.relabel_sequential(post)
if not np.array_equal(final, reference):
    raise RuntimeError("Supplemental trace differs from the saved segmentation. Inspect version/parameter differences before authoring figures.")

# Check the current function definition only; do not execute notebook cells.
namespace = {"image": image, "filters": filters, "measure": measure, "ndi": ndi,
             "feature": feature, "segmentation": segmentation, "np": np, "pd": pd}
function_cell = "".join(notebook["cells"][7]["source"])
tree = ast.parse(function_cell)
definition = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "segment_and_measure")
exec(compile(ast.Module(body=[definition], type_ignores=[]), "saved_notebook_function", "exec"), namespace)
current_labels, objects, current_threshold = namespace["segment_and_measure"]()
assert np.array_equal(current_labels, final)
assert current_threshold == otsu
border_excluded, interior_objects, _ = namespace["segment_and_measure"](exclude_edges=True)

components_after = measure.label(filled)
component_region = max(
    (r for r in measure.regionprops(components_after)
     if min(r.bbox[0], r.bbox[1]) > 8 and r.bbox[2] < 504 and r.bbox[3] < 504),
    key=lambda r: (len(np.unique(watershed[components_after == r.label])) - 1, r.area))
r0, c0, r1, c1 = component_region.bbox
margin = 12
r0, c0, r1, c1 = max(0, r0-margin), max(0, c0-margin), min(512, r1+margin), min(512, c1+margin)
roi = (slice(r0, r1), slice(c0, c1))

counts = {"raw_pixels": int(image.size), "raw_min": int(image.min()), "raw_max": int(image.max()),
          "raw_median": float(np.median(image)), "raw_mean": float(image.mean()),
          "smoothed_min": float(smoothed.min()), "smoothed_max": float(smoothed.max()),
          "otsu_threshold": otsu, "threshold_mask_pixels": int(threshold_mask.sum()),
          "initial_components_8_connected": int(connected.max()),
          "initial_components_below_40": int(np.sum(sizes[1:] < 40)),
          "initial_removed_pixels": int(threshold_mask.sum()-size_filtered.sum()),
          "components_retained_at_least_40": int(np.sum(sizes[1:] >= 40)),
          "mask_after_size_filter_pixels": int(size_filtered.sum()),
          "hole_pixels_added": int(filled.sum()-size_filtered.sum()),
          "filled_mask_pixels": int(filled.sum()), "distance_max_px": float(distance.max()),
          "markers": len(peaks), "watershed_nonzero_labels": int(np.sum(watershed_sizes[1:] > 0)),
          "unlabelled_filled_pixels": int(np.sum(filled & (watershed == 0))),
          "post_watershed_small_labels": int(np.sum((watershed_sizes[1:] > 0) & (watershed_sizes[1:] < 40))),
          "post_watershed_removed_pixels": int(np.sum((watershed > 0) & (post == 0))),
          "final_objects": len(objects), "final_pixels": int(np.sum(final > 0)),
          "final_foreground_percent": float(100*np.mean(final > 0)),
          "edge_objects": int(objects.touches_edge.sum()), "interior_objects": len(interior_objects),
          "area_min_px2": float(objects.area_px2.min()), "area_median_px2": float(objects.area_px2.median()),
          "area_max_px2": float(objects.area_px2.max()), "area_mean_px2": float(objects.area_px2.mean()),
          "diagnostic_roi_row_start_stop": [r0,r1], "diagnostic_roi_col_start_stop": [c0,c1],
          "reconstructed_labels_equal_saved_tiff": True, "current_function_equal_reconstruction": True}
manifest["trace"] = counts

def save(fig, filename, description):
    fig.savefig(ASSETS / filename, dpi=190, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    manifest["supplemental_figures"].append({"file": filename, "origin": "Supplemental diagnostic trace, not a saved notebook figure", "description": description})

def picture(ax, array, title, cmap="gray", **kwargs):
    artist = ax.imshow(array, cmap=cmap, interpolation="nearest", **kwargs)
    ax.set(title=title, xlabel="x / column (pixels)", ylabel="y / row (pixels)")
    return artist

# Use the notebook's human-review crop to show display scaling separately.
review_roi = (slice(128,256),slice(128,256))
fig, axes = plt.subplots(1,2,figsize=(8.2,3.6),layout="constrained")
picture(axes[0],image[review_roi],"Fixed display range: 0–255",vmin=0,vmax=255)
picture(axes[1],image[review_roi],"Auto display range: 7–108",vmin=7,vmax=108)
save(fig,"06_display_scaling.png","The same original crop displayed at two grayscale ranges; pixel values unchanged.")

fig, axes = plt.subplots(1,2,figsize=(8.2,3.6),layout="constrained")
display_max = float(image[roi].max())
picture(axes[0],image[roi],"Original diagnostic crop",vmin=0,vmax=display_max)
picture(axes[1],smoothed[roi],"Gaussian smoothing: sigma = 1 pixel",vmin=0,vmax=display_max)
save(fig,"07_gaussian_comparison.png","Original and smoothed diagnostic crop using exactly the same display limits.")

fig, ax = plt.subplots(figsize=(7.5,3.5),layout="constrained")
ax.hist(smoothed.ravel(),bins=256,color="#216869",alpha=.88)
for factor, colour in [(0.8,"#0072B2"),(1.0,"#D55E00"),(1.2,"#CC79A7")]:
    ax.axvline(otsu*factor,color=colour,linewidth=1.6,label=f"factor {factor:.1f}: {otsu*factor:.2f}")
ax.set(xlabel="Smoothed intensity (original 8-bit scale retained)",ylabel="Pixels per bin (log scale)",yscale="log",title="Histogram used for Otsu: smoothed image, 256 bins")
ax.legend(fontsize=9)
save(fig,"08_otsu_histogram.png","Gaussian-image histogram with the default threshold and two scaled thresholds.")

fig, axes = plt.subplots(2,2,figsize=(8.2,7.5),layout="constrained")
picture(axes[0,0],threshold_mask,f"A. Above Otsu: {threshold_mask.sum():,} pixels",vmin=0,vmax=1)
picture(axes[0,1],size_filtered,f"B. Remove components <40: {size_filtered.sum():,}",vmin=0,vmax=1)
picture(axes[1,0],filled,f"C. Fill enclosed holes: {filled.sum():,}",vmin=0,vmax=1)
changes = np.zeros((*image.shape,3),dtype=float)
changes[threshold_mask & ~size_filtered] = [0.90,0.45,0.05]
changes[filled & ~size_filtered] = [0.10,0.60,0.95]
axes[1,1].imshow(changes,interpolation="nearest")
axes[1,1].set(title=f"D. Orange: {counts['initial_removed_pixels']} removed\nBlue: {counts['hole_pixels_added']} filled",xlabel="x / column (pixels)",ylabel="y / row (pixels)")
save(fig,"09_mask_cleanup.png","Full-field threshold, component cleanup, hole filling, and changed-pixel map.")

fig, axes = plt.subplots(1,2,figsize=(8.5,3.8),layout="constrained")
im=picture(axes[0],distance,"Euclidean distance to mask background",cmap="magma",vmin=0,vmax=distance.max())
fig.colorbar(im,ax=axes[0],shrink=.8,label="Distance (pixels)")
picture(axes[1],distance,f"Selected markers: {len(peaks)}",cmap="magma",vmin=0,vmax=distance.max())
axes[1].scatter(peaks[:,1],peaks[:,0],s=5,c="#00D5FF",marker="+")
save(fig,"10_distance_seeds.png","Distance-transform image and the default seed coordinates overlaid in cyan.")

fig, axes = plt.subplots(2,2,figsize=(8.0,7.0),layout="constrained")
picture(axes[0,0],image[roi],"A. Original diagnostic crop",vmin=0,vmax=display_max)
picture(axes[0,1],distance[roi],"B. Distance and seed locations",cmap="magma")
sel=(peaks[:,0]>=r0)&(peaks[:,0]<r1)&(peaks[:,1]>=c0)&(peaks[:,1]<c1)
axes[0,1].scatter(peaks[sel,1]-c0,peaks[sel,0]-r0,s=35,c="#00D5FF",marker="+")
for n,(row,col) in enumerate(peaks[sel],1):
    axes[0,1].text(col-c0+1,row-r0,str(n),color="cyan",fontsize=8)
picture(axes[1,0],color.label2rgb(watershed[roi],image=image[roi],bg_label=0,alpha=.5),"C. Watershed partitions before size filter")
picture(axes[1,1],color.label2rgb(final[roi],image=image[roi],bg_label=0,alpha=.5),"D. Final surviving labels")
save(fig,"11_watershed_crop.png",f"Diagnostic crop at rows {r0}:{r1}, columns {c0}:{c1}; seed positions and watershed partitions.")

edge_labels=objects.loc[objects.touches_edge,"object_id"].to_numpy()
edge_mask=np.isin(final,edge_labels)
overlay=color.gray2rgb(image.astype(float)/255)
overlay[(final>0)&~edge_mask]=.55*overlay[(final>0)&~edge_mask]+.45*np.array([0.1,.7,.9])
overlay[edge_mask]=.3*overlay[edge_mask]+.7*np.array([1,.25,.05])
fig, axes=plt.subplots(1,2,figsize=(8.2,3.6),layout="constrained")
picture(axes[0],overlay,"Default: orange = 26 edge-touching labels")
picture(axes[1],color.label2rgb(border_excluded,image=image,bg_label=0,alpha=.4),f"Exclude edges: {len(interior_objects)} objects")
save(fig,"12_border_policy.png","Default final labels with edge labels highlighted and a separate border-excluded analysis.")

(ASSETS/"figure_manifest.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps(counts,indent=2))
print("Saved notebook figures:",len(manifest["saved_figures"]),"| Supplemental figures:",len(manifest["supplemental_figures"]))
print("Assets:",ASSETS)
