"""Bundle the microscopy LaTeX source and figures for Overleaf."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

reports = Path(__file__).resolve().parent
archive = reports / "microscopy_overleaf.zip"
files = [reports / "microscopy_analysis_report.tex",
         reports / "microscopy_OVERLEAF_README.md",
         *sorted((reports / "microscopy_figures").glob("*.png")),
         reports / "microscopy_figures/figure_manifest.json"]

with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
    for path in files:
        bundle.write(path, path.relative_to(reports))

check_dir = Path("/private/tmp/lec2026-microscopy-overleaf-check")
check_dir.mkdir(exist_ok=True)
with ZipFile(archive) as bundle:
    bundle.extractall(check_dir)
(check_dir / "build").mkdir(exist_ok=True)

compiled = Path("/private/tmp/lec2026-microscopy-report-build/microscopy_analysis_report.pdf")
shutil.copyfile(compiled, reports / "microscopy_analysis_report.pdf")
print(f"Bundle: {archive.name}; {len(files)} files; {archive.stat().st_size:,} bytes")
print(f"Isolated compile directory: {check_dir}")
