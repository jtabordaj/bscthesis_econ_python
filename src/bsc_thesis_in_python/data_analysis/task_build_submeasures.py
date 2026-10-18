import pandas as pd
from pathlib import Path

from bsc_thesis_in_python.config import BLD
from bsc_thesis_in_python.data_management.utilities import validate_input

RENAME_MAP_TECH = {
    "VI1R8C2": "PM", 
    "VI2R8C2": "PM1718", 
    "VI3R5C2": "NCPM1718"
}

RENAME_MAP_STABILITY = {
    "I1R4C2N": "RI",
    "I1R4C2M": "II",
}


def _calculate_firm_share(variable: pd.Series) -> pd.Series:
    """Helper function to calculate the percentage share of a firm within its industry.

    Args:
        variable (pd.Series): Series representing a specific economic variable.
    
    Returns:
        pd.Series: Series where each value is a fraction over the total (value/total)*100.
    """
    return (variable / variable.sum()) * 100


def calculate_concentration_submeasures(data: pd.DataFrame) -> pd.DataFrame:
    """Calculates firm-level market shares for various economic variables.

    Args:
        data (pd.DataFrame): Dataframe containing industry-separated firm data.

    Returns:
        pd.DataFrame: Dataframe with added columns "MS" Market Share, 
        "MSA" Market Share of Innovation Activities, "LDS" Labor Demand Share, 
        and "SS" Supply Share.
    """
    validate_input(data, pd.DataFrame, "data")

    df = data.copy()

    df["MS"] = _calculate_firm_share(df["I3R2C1"])
    df["MSA"] = _calculate_firm_share(df["II1R10C2"])
    df["LDS"] = _calculate_firm_share(df["PERTOTAL"])
    df["SS"] = _calculate_firm_share(df["PRODBIND"])

    return df


def rename_technological_variables(data: pd.DataFrame) -> pd.DataFrame:
    """Renames survey answers about protection mechanisms to descriptive labels.

    Args:
        data (pd.DataFrame): Dataframe containing raw survey column names.

    Returns:
        pd.DataFrame: Dataframe with renamed columns.
    """
    return data.rename(columns=RENAME_MAP_TECH)


def rename_stability_variables(data: pd.DataFrame) -> pd.DataFrame:
    """Renames survey answers about innovation nature to descriptive labels.

    Args:
        data (pd.DataFrame): Dataframe containing raw survey column names.

    Returns:
        pd.DataFrame: Dataframe with renamed columns: RI (Internal) and II (External).
    """
    return data.rename(columns=RENAME_MAP_STABILITY)


def task_calculate_submeasures(
    depends_on: Path = BLD / "split_data.xlsx",
    produces: Path = BLD / "split_data_with_submeasures.xlsx",
) -> None:
    """Manages the generation of firm-level submeasures across all industries.

    This task reads a file (.xlsx) with separated industry, applies
    variable renaming and calculations, and saves results back to a
    multi-sheet (.xlsx) file.
    """
    all_sectors = pd.read_excel(depends_on, sheet_name=None)

    with pd.ExcelWriter(produces) as writer:
        for sector_name, df in all_sectors.items():
            processed = rename_technological_variables(df)
            processed = rename_stability_variables(processed)
            processed = calculate_concentration_submeasures(processed)
            processed.to_excel(writer, sheet_name=str(sector_name), index=False)


if __name__ == "__main__":
    task_calculate_submeasures()
