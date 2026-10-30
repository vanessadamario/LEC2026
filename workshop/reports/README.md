# Dataset reports

## Microscopy: illustrated analysis walkthrough

[LaTeX source](microscopy_analysis_report.tex) · [Compiled PDF](microscopy_analysis_report.pdf) · [Overleaf upload ZIP](microscopy_overleaf.zip)

The report explains intensity inspection, display scaling, Gaussian smoothing, Otsu thresholding, connected-component size filtering, hole filling, the distance transform, seed detection, watershed, border policy, measurements, sensitivity, and visual validation. It uses all five saved notebook plots and seven labelled diagnostic views.

Upload the ZIP as an Overleaf project, select `microscopy_analysis_report.tex`, and use pdfLaTeX. The source requires the accompanying `microscopy_figures/` folder. See [microscopy upload instructions](microscopy_OVERLEAF_README.md).

## Oceanography: dataset description and analysis plan

[LaTeX source](oceanography_dataset_report.tex) · [Compiled PDF](oceanography_dataset_report.pdf)

The report documents the GO-SHIP P02W teaching subset, the complete twelve-field input dictionary, quality flags and acceptance policy, profile coverage, analytical and educational goals, reference summaries, interactive tool, limitations, and sources. Appendices include the source-query specification, loading example, derived-output dictionary, and glossary.

### Upload the oceanography report to Overleaf

1. Create a blank project and upload `oceanography_dataset_report.tex`.
2. Set that file as the project's **Main document**.
3. Choose **pdfLaTeX** as the compiler and recompile. Overleaf normally repeats compilation as needed to resolve the contents and cross-references.

The source is self-contained: the bibliography and diagram are embedded. No dataset, external image, `.bib` file, or shell escape is needed. You can edit the title, author, and date in the preamble. The PDF is a convenience preview; the `.tex` file is the editable deliverable.

The report describes the October 13, 2026 CSV snapshot and sources reviewed on October 23, 2026. It includes descriptive summaries, without embedding the raw observation table. The notebooks were not rerun to produce the report.
