# Microscopy candidates and provenance

Prepared notebook: `notebooks/03_microscopy.ipynb`. Primary runtime: CloudBank Classroom, Python 3.10+ kernel, CPU. Dependency check is read-only; installation is an instructor setup step.

| Candidate | Teaching question | Access / license | Fit |
|---|---|---|---|
| scikit-image human_mitosis | How do threshold, seed spacing, and edge rules affect measured objects? | One 512×512 grayscale field, CC0, David Root. Bundled original TIFF. | Primary: lightweight, visible segmentation changes; no reference mask or pixel-size calibration. |
| scikit-image quantitative phase cell | How does physical calibration change area interpretation, and how do background artifacts affect thresholding? | One 660×550 grayscale image, CC0; reported pixel spacing 0.107 µm. | Follow-up: one cell with banding artifacts; not a population dataset. |
| BloodMNIST | Can image features classify eight normal blood-cell categories? Which classes are confused? | 17,092 resized images, CC BY 4.0, official Zenodo distribution. | Later classification exercise. Preserve official splits; 28×28 images lose detail and labels concern cell types, not disease diagnosis. |

Primary documentation:

- [scikit-image data API](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.human_mitosis)
- [Image licensing discussion](https://github.com/CellProfiler/examples/issues/41)
- [Moffat et al. (2006) source paper](https://doi.org/10.1016/j.cell.2006.01.040)
- [Pinned scikit-image dataset registry](https://github.com/scikit-image/scikit-image/blob/v0.25.2/skimage/data/_registry.py)
- [MedMNIST project](https://medmnist.com/)
- [Official MedMNIST+ dataset](https://zenodo.org/records/10519652)

Bundled file: `data/microscopy/mitosis.tif`, 233,336 bytes. Download URL:
`https://gitlab.com/scikit-image/data/-/raw/2cdc5ce89b334d28f06a58c9f0ca21aa6992a5ba/AS_09125_050116030001_D03f00d0.tif`

SHA-256: `2751ba667c4067c5d30817cff004aa06f6f6287f1cdbb5b8c9c6a500308cb456`.
The hash matches the scikit-image v0.25.2 registry. The image is unchanged. Segmentation outputs are derived, unvalidated teaching measurements. No synthetic microscopy image is substituted.

Dependencies: numpy, pandas, matplotlib, scipy, scikit-image, ipywidgets; requests only for standalone image download fallback. Output files record parameters, source hash, and package versions.
