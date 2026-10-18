import pandas as pd
from pathlib import Path

from bsc_thesis_in_python.config import BLD
from bsc_thesis_in_python.data_management.utilities import validate_input


def merge_datasets(
    left: pd.DataFrame, right: pd.DataFrame, on_columns: list[str]
) -> pd.DataFrame:
    """Merge two dataframes on specific columns and fill NAs with 0.

    Args:
        left (pd.DataFrame): The left dataframe (e.g., EAM).
        right (pd.DataFrame): The right dataframe (e.g., EDIT).
        on_columns (list[str]): List of column names to join on.

    Returns:
        pd.DataFrame: The merged dataframe with NAs filled with 0.
    """
    validate_input(left, pd.DataFrame, "left")
    validate_input(right, pd.DataFrame, "right")
    validate_input(on_columns, list, "on_columns")

    merged = pd.merge(left, right, on=on_columns, how="inner")
    
    return merged.fillna(0)


def task_merge_surveys(
    depends_on: dict[str, Path] = {
        "edit_path": BLD / "edit_prepared.feather",
        "eam_path": BLD / "eam_prepared.feather",
    },
    produces: Path = BLD / "merged_data.feather",
) -> None:
    """Merge prepared EDIT and EAM surveys.

    Reads feather files from the build directory, merges them, and saves
    the result as a feather file.
    """
    merge_keys = ["NORDEMP", "CIIU4"]

    edit = pd.read_feather(depends_on["edit_path"])
    eam = pd.read_feather(depends_on["eam_path"])
    merged = merge_datasets(eam, edit, merge_keys)

    merged.to_feather(produces)


if __name__ == "__main__":
    task_merge_surveys()
