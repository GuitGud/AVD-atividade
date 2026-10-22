"""Executa a EDA local e atualiza os CSVs e as saídas do notebook."""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "notebooks" / "eda.ipynb"
notebook = nbformat.read(path, as_version=4)
NotebookClient(
    notebook,
    timeout=300,
    kernel_name="python3",
    resources={"metadata": {"path": str(ROOT)}},
).execute()
nbformat.write(notebook, path)
print("EDA executada. Notebook e datasets atualizados.")
