from pathlib import Path
import pandas as pd

import pyreadstat

from bsc_thesis_in_python.config import BLD
from bsc_thesis_in_python.data_management.utilities import validate_input

EDIT_COLS = [
    "NORDEMP",
    "CIIU4",
    "I1R1C1N",
    "I1R1C2N",
    "I1R2C1N",
    "I1R2C2N",
    "I1R3C1N",
    "I1R3C2N",
    "I1R4C2N",
    "I1R1C1M",
    "I1R1C2M",
    "I1R2C1M",
    "I1R2C2M",
    "I1R3C1M",
    "I1R3C2M",
    "I1R4C2M",
    "I2R3C1",
    "I3R1C1",
    "I3R2C1",
    "II1R10C1",
    "II1R10C2",
    "IV1R11C1",
    "IV1R11C2",
    "IV1R11C3",
    "IV1R11C4",
    "VI1R1C1",
    "VI1R1C2",
    "VI1R2C1",
    "VI1R2C2",
    "VI1R3C1",
    "VI1R3C2",
    "VI1R4C1",
    "VI1R4C2",
    "VI1R5C1",
    "VI1R5C2",
    "VI1R6C1",
    "VI1R6C2",
    "VI1R8C2",
    "VI2R1C1",
    "VI2R1C2",
    "VI2R2C1",
    "VI2R2C2",
    "VI2R3C1",
    "VI2R3C2",
    "VI2R4C1",
    "VI2R4C2",
    "VI2R5C1",
    "VI2R5C2",
    "VI2R6C1",
    "VI2R6C2",
    "VI2R8C2",
    "VI3R1C1",
    "VI3R1C2",
    "VI3R2C1",
    "VI3R2C2",
    "VI3R3C1",
    "VI3R3C2",
    "VI3R4C1",
    "VI3R4C2",
    "VI3R5C2",
]

EAM_COLS = [
    "NORDEMP",
    "nordest",
    "dpto",
    "CIIU4",
    "c6r5c1",
    "c6r5c3",
    "c7r10c1",
    "c7c7r2",
    "c7c7r3",
    "PRODBR2",
    "PRODBIND",
    "ACTIVFI",
    "VALORVEN",
    "PERTOTAL",
    "VALAGRI",
]

def prepare_dataset(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Filter and standardize a dataset.
    Args:
        df: The raw input dataframe.
        columns: List of column names to keep.
    
    Returns:
        pd.DataFrame: The cleaned and filtered dataframe.
    """
    validate_input(columns, list, "columns")

    df = df.copy()
    df.columns = df.columns.str.upper()
    req_columns = [c.upper() for c in columns]

    return df[req_columns]

def task_prepare_edit_data(
    depends_on: Path = BLD / "EDIT.dta",
    produces: Path = BLD / "edit_prepared.feather" 
) -> None:
    """Manages the retrieval of EDIT data.

    This task reads and processes the EDIT survey data based on the
    logic required for the project. Returns one prepared dataset (.feather).
    """
    df, _ = pyreadstat.read_dta(depends_on)
    cleaned_df = prepare_dataset(df, EDIT_COLS)
    cleaned_df.to_feather(produces)


def task_prepare_eam_data(
    depends_on: Path = BLD / "EAM.dta",
    produces: Path = BLD / "eam_prepared.feather"
) -> None:
    """Manages the retrieval of EAM data.

    This task reads and processes the EAM survey data based on the
    logic required for the project. Returns one prepared dataset (.feather).
    """
    df, _ = pyreadstat.read_dta(depends_on)
    cleaned_df = prepare_dataset(df, EAM_COLS)
    cleaned_df.to_feather(produces)

if __name__ == "__main__":
    task_prepare_edit_data()
    task_prepare_eam_data()
