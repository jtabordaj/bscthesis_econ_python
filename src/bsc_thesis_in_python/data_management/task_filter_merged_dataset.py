import pandas as pd
from pathlib import Path

from bsc_thesis_in_python.config import BLD
from bsc_thesis_in_python.data_management.utilities import validate_input

REQUIRED_COLS = [
    "NORDEMP",
    "DPTO",
    "CIIU4",
    "I3R2C1",
    "II1R10C2",
    "PERTOTAL",
    "PRODBIND",
    "VI1R8C2",
    "VI2R8C2",
    "VI3R5C2",
    "I1R4C2N",
    "I1R4C2M",
]

CIIU_LOWER_BOUND = 1011
CIIU_UPPER_BOUND = 3530

def filter_and_transform(
    df: pd.DataFrame, columns: list[str], lb: int, ub: int
) -> pd.DataFrame:
    """Subset the merged dataset into the required scope of study.

    Args:
        df (pd.DataFrame): Dataframe containing the merge of EDIT and EAM Surveys.
        columns (list[str]): Variables of interest given the scope of research.
        lb (int): Numeric lower bound of the desired CIIU4 classification scope.
        ub (int): Numeric upper bound of the desired CIIU4 classification scope.

    Returns:
        pd.DataFrame: Filtered and transformed dataset.
    """
    validate_input(df, pd.DataFrame, "df")
    validate_input(columns, list, "columns")
    validate_input(lb, int, "lb") 
    validate_input(ub, int, "ub")

    df = df.copy()

    df = df[df["CIIU4"].between(lb, ub)]

    df = df[columns]

    df = df.rename(columns={"DPTO": "ID_DEPTO"})
    df["ID_DEPTO"] = df["ID_DEPTO"].astype(str)

    replace_map = {"5": "05", "8": "08"}
    df["ID_DEPTO"] = df["ID_DEPTO"].replace(replace_map)

    return df

def task_prepare_merged_dataset(
    depends_on: Path = BLD / "merged_data.feather",
    produces: Path = BLD / "final_data.feather",
) -> None:
    """Prepare the final merged dataset.

    Receives the merged dataset (.feather), performs transformations based on 
    CIIU4 bounds, and returns the final dataset (.feather).
    """

    df = pd.read_feather(depends_on)

    filtered = filter_and_transform(
        df, 
        REQUIRED_COLS, 
        CIIU_LOWER_BOUND, 
        CIIU_UPPER_BOUND
    )

    filtered.to_feather(produces)

if __name__ == "__main__":
    task_prepare_merged_dataset()
