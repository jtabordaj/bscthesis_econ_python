"""Tasks for compiling the paper and presentation(s)."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytask

from bsc_thesis_in_python.config import DOCUMENTS, ROOT

for fmt, produces in {
    "pdf": ROOT / "paper.pdf",
    "html": ROOT / "_build" / "html" / "index.html",
}.items():

    @pytask.task(id=f"paper-{fmt}")
    def task_compile_paper(
        paper_md: Path = DOCUMENTS / "paper.md",
        myst_yml: Path = ROOT / "myst.yml",
        figure: Path = DOCUMENTS / "public" / "kmeans_cluster_plot.png",
        refs: Path = DOCUMENTS / "refs.bib",
        produces: Path = produces,
    ) -> None:
        """Compile the paper from MyST Markdown using Jupyter Book 2.0."""
        fmt = produces.suffix.lstrip(".")
        subprocess.run(
            ("jupyter", "book", "build", f"--{fmt}"),
            check=True,
            cwd=ROOT.absolute(),
        )
        if fmt == "pdf":
            build_pdf = ROOT / "_build" / "exports" / "paper.pdf"
            shutil.copy(build_pdf, produces)
