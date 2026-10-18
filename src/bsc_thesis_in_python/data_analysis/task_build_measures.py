import pandas as pd
from pathlib import Path

from bsc_thesis_in_python.config import BLD
from bsc_thesis_in_python.data_management.utilities import validate_input


def _calculate_hhi(series: pd.Series) -> float:
    """Helper function to calculate the Herfindahl-Hirschman Index (HHI).

    Args:
        series (pd.Series): Series representing share percentages.

    Returns:
        float: The sum of squared shares.
    """
    validate_input(series, pd.Series, "series")
    return (series**2).sum()


def calculate_concentration_measure(df: pd.DataFrame) -> dict[str, float]:
    """Calculate the CON index based on the geometric mean of four HH Indices.

    Args:
        df (pd.DataFrame): Dataframe containing market share variables (MS, MSA, LDS, SS).

    Returns:
        dict[str, float]: Dictionary containing the Herfindahl-Hirschman Index for each share
        variable, and the geometric mean CON index.
    """
    hh_ms = _calculate_hhi(df["MS"])
    hh_msa = _calculate_hhi(df["MSA"])
    hh_lds = _calculate_hhi(df["LDS"])
    hh_ss = _calculate_hhi(df["SS"])

    con = (hh_ms * hh_msa * hh_lds * hh_ss) ** 0.25

    return {"HHms": hh_ms, "HHmsa": hh_msa, "HHlds": hh_lds, "HHss": hh_ss, "CON": con}


def calculate_stability_measure(df: pd.DataFrame) -> dict[str, float]:
    """Calculate stability index (STA) based on internal (RI) and external (II) innovation.

    Args:
        df (pd.DataFrame): Dataframe containing per-firm count of Radical (RI) and
        Incremental (II) innovations.

    Returns:
        dict[str, float]: Dictionary containing the share of radical (sr), and
        incremental innovations (si), together with the STA index.
    """
    sum_ri = df["RI"].sum()
    sum_ii = df["II"].sum()
    total_innovation = sum_ri + sum_ii

    if total_innovation == 0:
        return {"sr": 0.0, "si": 0.0, "STA": 0.0}

    sr = sum_ri / total_innovation
    si = sum_ii / total_innovation

    return {"sr": sr, "si": si, "STA": sr - si}


def calculate_technological_opportunities(df: pd.DataFrame) -> dict[str, float]:
    """Calculate Technological Opportunities Index (TO).

    Args:
        df (pd.DataFrame): Dataframe containing protection mechanism variables.

    Returns:
        dict[str, float]: Dictionary containing the TO index.
    """
    denominator = df["PM"].sum()

    if denominator == 0:
        return {"TO": 0.0}

    numerator = df["PM1718"].sum() + df["NCPM1718"].sum()

    return {"TO": numerator / denominator}


def task_calculate_measures(
    depends_on: Path = BLD / "split_data_with_submeasures.xlsx",
    produces: Path = BLD / "industry_measures.csv",
) -> None:
    """Manages the calculation of aggregate industry-level measures.

    This task reads the processed, industry-separated (.xlsx) firm-level data,
    calculates Concentration (CON), Stability (STA), and Technological Opportunity (TO)
    indices per industry, and saves the consolidated results to a new table (.csv).
    """
    all_sectors = pd.read_excel(depends_on, sheet_name=None)
    results = []

    for sector, df in all_sectors.items():
        metrics = {"CIIU4": str(sector)}
        metrics.update(calculate_concentration_measure(df))
        metrics.update(calculate_stability_measure(df))
        metrics.update(calculate_technological_opportunities(df))
        results.append(metrics)

    final_df = pd.DataFrame(results)
    final_df.to_csv(produces, index=False)


if __name__ == "__main__":
    task_calculate_measures()
