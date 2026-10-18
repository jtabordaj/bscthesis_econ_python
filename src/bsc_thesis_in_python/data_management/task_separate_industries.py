import pandas as pd
from pathlib import Path

from bsc_thesis_in_python.config import BLD
from bsc_thesis_in_python.data_management.utilities import validate_input

MIN_OBSERVATIONS = 20
GROUP_COLUMN = "CIIU4"

def split_industries(
    df: pd.DataFrame, group_col: str, min_obs: int
) -> dict[str, pd.DataFrame]:
    """Separate a dataset into a dictionary of dataframes by group.

    Args:
        df (pd.DataFrame): Dataframe with filtered and merged information.
        group_col (str): Column to be used as split criteria.
        min_obs (int): Minimum firms per industry to include in the split.

    Returns:
        dict[str, pd.DataFrame]: Dictionary where keys are industry codes and 
        values are the corresponding dataframes.
    """
    validate_input(df, pd.DataFrame, "df")
    validate_input(group_col, str, "group_col")
    validate_input(min_obs, int, "min_obs")

    grouped = dict(tuple(df.groupby(group_col)))

    return {k: v for k, v in grouped.items() if len(v) > min_obs}


def task_split_industries(
    depends_on: Path = BLD / "final_data.feather",
    produces: Path = BLD / "split_data.xlsx",
) -> None:
    """Split the merged dataset into separate CIIU4 industries in Excel.

    Reads the final dataset (.feather), splits it by sector, and writes 
    an Excel file with one sheet per sector.
    """
    main = pd.read_feather(depends_on)

    filtered_sectors = split_industries(
        main, group_col=GROUP_COLUMN, min_obs=MIN_OBSERVATIONS
    )

    with pd.ExcelWriter(produces) as writer:
        for sector_name, df in filtered_sectors.items():
            df.to_excel(writer, sheet_name=str(sector_name), index=False)


if __name__ == "__main__":
    task_split_industries()
