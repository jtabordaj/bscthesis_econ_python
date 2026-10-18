import zipfile

from bsc_thesis_in_python.config import BLD, SRC

from pathlib import Path

def task_unzip_data(
    depends_on: Path = SRC / "data" / "data.zip",
    produces: dict[str, Path] = {"EDIT": BLD / "EDIT.dta", "EAM": BLD / "EAM.dta"},
) -> None:
    """Unzip original data to the build directory."""
    with zipfile.ZipFile(depends_on, "r") as zip_ref:
        for path in produces.values():
            zip_ref.extract(path.name, path=path.parent)


if __name__ == "__main__":
    task_unzip_data()
