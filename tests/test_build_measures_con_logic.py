import numpy as np
import pandas as pd
import pytest

from src.bsc_thesis_in_python.data_analysis.task_build_measures import (
    _calculate_hhi,
    calculate_concentration_measure,
)


def test_calculate_hhi_monopoly():
    """Tests that the HHI helper function correctly handles monopoly cases.

    Test will pass if `_calculate_hhi()` correctly returns a HHI of 1.0
    if the market share is that of a monopoly.
    """
    monopolyexample = pd.Series([1.0])

    assert _calculate_hhi(monopolyexample) == 1.0


def test_calculate_hhi_intermediate():
    """Tests that the HHI helper function correctly handles intermediate cases.

    Test will pass if, for a random set of non-monopoly, non-perfect-competition shares,
    `_calculate_hhi()` correctly returns its expected HHI.
    """
    np.random.seed(41)  # noqa: NPY002
    intermediateexample = pd.Series(np.random.dirichlet(np.ones(5)))  # noqa: NPY002
    expected_hhi = (intermediateexample**2).sum()

    assert _calculate_hhi(intermediateexample) == pytest.approx(expected_hhi)


def test_calculate_hhi_perfect_competition():
    """Tests that the HHI helper function correctly handles perfect competition.

    Test will pass if, for a set of large shares that resembles perfect competition,
    `_calculate_hhi()` correctly returns its expected, almost-zero, HHI.
    """
    n = 100000
    share_value = 1 / n
    perfectcompetitionexample = pd.Series([share_value] * n)

    expected_hhi = 1 / n

    assert _calculate_hhi(perfectcompetitionexample) == pytest.approx(expected_hhi)


def test_con_monopoly_case():
    """Tests that the 'CON' calculation function correctly handles monopoly cases.

    Test will pass if, for a set of large shares that resembles perfect competition,
    `calculate_concentration_measure()` correctly returns its expected value of 1.0.
    """
    monopolyexample = [1.0]
    df = pd.DataFrame(
        {
            "MS": monopolyexample,
            "MSA": monopolyexample,
            "LDS": monopolyexample,
            "SS": monopolyexample,
        }
    )
    result = calculate_concentration_measure(df)

    assert result["CON"] == 1.0


def test_con_intermediate_case_random():
    """Tests that the 'CON' calculation function correctly handles intermediate cases.

    Test will pass if, for a set of for a random set of non-monopoly, non-perfect-competition
    shares, `calculate_concentration_measure()` correctly returns its expected CON value.
    """
    np.random.seed(42)  # noqa: NPY002
    n = 20

    shares_ms = np.random.dirichlet(np.ones(n))  # noqa: NPY002
    shares_msa = np.random.dirichlet(np.ones(n))  # noqa: NPY002
    shares_lds = np.random.dirichlet(np.ones(n))  # noqa: NPY002
    shares_ss = np.random.dirichlet(np.ones(n))  # noqa: NPY002

    df = pd.DataFrame(
        {"MS": shares_ms, "MSA": shares_msa, "LDS": shares_lds, "SS": shares_ss}
    )
    hhi_ms = (shares_ms**2).sum()
    hhi_msa = (shares_msa**2).sum()
    hhi_lds = (shares_lds**2).sum()
    hhi_ss = (shares_ss**2).sum()
    expected_con = (hhi_ms * hhi_msa * hhi_lds * hhi_ss) ** 0.25

    result = calculate_concentration_measure(df)

    assert result["CON"] == pytest.approx(expected_con, abs=1e-5)
    assert result["HHms"] == pytest.approx(hhi_ms)
    assert result["HHmsa"] == pytest.approx(hhi_msa)
    assert result["HHlds"] == pytest.approx(hhi_lds)
    assert result["HHss"] == pytest.approx(hhi_ss)


def test_con_perfect_competition_case():
    """Tests that the CON calculation function correctly handles perfect competition cases.

    Test will pass if, for a set of large shares that resembles perfect competition,
    `calculate_concentration_measure()` correctly returns its expected value of 0.
    """
    n = 100000
    share_value = 1 / n
    perfectcompetitionexample = pd.Series([share_value] * n)
    df = pd.DataFrame(
        {
            "MS": perfectcompetitionexample,
            "MSA": perfectcompetitionexample,
            "LDS": perfectcompetitionexample,
            "SS": perfectcompetitionexample,
        }
    )
    hhi_ms = (df["MS"] ** 2).sum()
    hhi_msa = (df["MSA"] ** 2).sum()
    hhi_lds = (df["LDS"] ** 2).sum()
    hhi_ss = (df["SS"] ** 2).sum()

    expected_con = (hhi_ms * hhi_msa * hhi_lds * hhi_ss) ** 0.25
    result = calculate_concentration_measure(df)

    assert result["CON"] == pytest.approx(expected_con, abs=1e-9)
    assert result["HHms"] == pytest.approx(hhi_ms, abs=1e-9)
    assert result["HHmsa"] == pytest.approx(hhi_msa, abs=1e-9)
    assert result["HHlds"] == pytest.approx(hhi_lds, abs=1e-9)
    assert result["HHss"] == pytest.approx(hhi_ss, abs=1e-9)
