"""Execute the real notebook with the caller's Python kernel; inspect core outputs."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

p = Path(__file__).resolve().parents[1] / 'notebooks/01_human_biology.ipynb'
nb = nbformat.read(str(p), as_version=4)
km = KernelManager(kernel_name='python3')
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
NotebookClient(nb, km=km, timeout=120, resources={'metadata': {'path': str(p.parent)}}).execute()
errors = [o for c in nb.cells if c.cell_type == 'code' for o in c.get('outputs', []) if o.output_type == 'error']
if errors:
    raise RuntimeError(errors)
nbformat.write(nb, str(p))
print('Notebook executed with', sys.executable)
print('Executed code cells:', sum(c.cell_type == 'code' and c.execution_count is not None for c in nb.cells))
for c in nb.cells:
    for o in c.get('outputs', []):
        if o.output_type == 'stream' and any(t in o.text for t in ['Difference of means', 'Loaded ', 'Ready:']):
            print(o.text.strip())
outputs = p.parent / 'outputs/01_human_biology'
expected = ['age_band_comparison.csv', 'age_cholesterol.png', 'cholesterol_group_summary.csv', 'missingness.csv']
for filename in expected:
    artifact = outputs / filename
    if not artifact.exists() or artifact.stat().st_size == 0:
        raise RuntimeError('Missing artifact: ' + str(artifact))
print('All four output artifacts present and nonempty.')
