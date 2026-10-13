"""Package authored workshop materials and source data; exclude development caches."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT.parent / "faculty_ai_workshop.zip"
EXCLUDED_DIRECTORIES = {".cache", "__pycache__", "tools", "scripts", "previews", "outputs", "results", "verification"}

with ZipFile(DESTINATION, "w", ZIP_DEFLATED) as archive:
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if not path.is_file() or any(p in EXCLUDED_DIRECTORIES for p in relative.parts):
            continue
        # Keep the optional output validator; builders are development artifacts.
        if path.suffix == ".py" and path.name != "validate_outputs.py":
            continue
        archive.write(path, str(Path("workshop") / relative))
print(str(DESTINATION))
print(f"Archive size: {DESTINATION.stat().st_size:,} bytes")
