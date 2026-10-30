# Microscopy report: Overleaf upload

1. In Overleaf, choose **New Project → Upload Project** and upload `microscopy_overleaf.zip`.
2. Set **microscopy_analysis_report.tex** as the main document.
3. Select **pdfLaTeX** and recompile.

Alternatively, upload the `.tex` file and the complete `microscopy_figures/` folder into a blank project. Keep the folder name and relative paths unchanged. Uploading the `.tex` file alone will leave the figures unavailable.

The report includes the five plots saved in the microscopy notebook and seven clearly labelled supplemental diagnostic figures. The bibliography is embedded in the `.tex` file. The ZIP contains the LaTeX source, figures, figure-provenance manifest, and these instructions. It requires no raw dataset, notebook, Python installation, external `.bib` file, or shell escape to compile.

The separate `microscopy_analysis_report.pdf` is the compiled preview. The report covers the entire pipeline from intensity inspection through final measurements, parameter sensitivity, crop review, and exports.

Figure provenance is documented in the report appendix and `microscopy_figures/figure_manifest.json`. Saved notebook figures were extracted unchanged; diagnostic figures were generated separately and the default reconstruction was matched to the saved label image. The original notebook and its exported datasets were preserved.
