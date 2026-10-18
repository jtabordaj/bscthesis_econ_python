import numpy as np
import pandas as pd
import pytest

from src.bsc_thesis_in_python.data_analysis.task_build_measures import (
    calculate_stability_measure,
)


def test_sta_zero_innovation_case():
    """
    Test that the STA calculation correctly handles industries with no reported innovations.

    Test will pass if `calculate_stability_measure()` returns a 'STA' metric of 0, and both shares
    ('rs', 'ri') return 0.
    """
    np.random.seed(47)  # noqa: NPY002

    zeroinnovationmarket = np.zeros(20, dtype=int)

    df = pd.DataFrame({"RI": zeroinnovationmarket, "II": zeroinnovationmarket})

    result = calculate_stability_measure(df)

    assert result["STA"] == 0.0
    assert result["sr"] == 0.0
    assert result["si"] == 0.0


def test_sta_radical_only_case():
    """
    Test that the STA calculation correctly handles industries of radical innovations only.

    Test will pass if `calculate_stability_measure()` returns a 'STA' metric of 1, an 'rs' of 1,
    and an 'ri' of 0.
    """
    np.random.seed(48)  # noqa: NPY002

    zeroinnovationmarket = np.zeros(20, dtype=int)
    radicalinnovationmarket = np.random.randint(0, 100, 20)  # noqa: NPY002

    df = pd.DataFrame({"RI": radicalinnovationmarket, "II": zeroinnovationmarket})

    result = calculate_stability_measure(df)

    assert result["STA"] == 1.0
    assert result["sr"] == 1.0
    assert result["si"] == 0.0


def test_sta_incremental_only_case():
    """
    Test that the STA calculation correctly handles industries of incremental innovations only.

    Test will pass if `calculate_stability_measure()` returns a 'STA' metric of -1, an 'rs' of 0,
    and an 'ri' of 1.
    """
    np.random.seed(49)  # noqa: NPY002

    incrementalinnovationmarket = np.random.randint(0, 100, 20)  # noqa: NPY002
    zeroinnovationmarket = np.zeros(20, dtype=int)

    df = pd.DataFrame({"RI": zeroinnovationmarket, "II": incrementalinnovationmarket})

    result = calculate_stability_measure(df)

    assert result["STA"] == -1.0
    assert result["sr"] == 0.0
    assert result["si"] == 1.0


def test_sta_intermediate_case_random():
    """
    Test that the STA calculation correctly handles industries of various innovation types.

    Test will pass if `calculate_stability_measure()` returns an expected 'STA', 'rs', and 'ri',
    given a randomly generated sample of both radical and incremental innovations.
    """
    np.random.seed(50)  # noqa: NPY002

    ri_counts = np.random.randint(0, 100, 20)  # noqa: NPY002
    ii_counts = np.random.randint(0, 100, 20)  # noqa: NPY002

    df = pd.DataFrame({"RI": ri_counts, "II": ii_counts})

    total_ri = ri_counts.sum()
    total_ii = ii_counts.sum()
    total_in = total_ri + total_ii

    expected_sr = total_ri / total_in
    expected_si = total_ii / total_in
    expected_sta = expected_sr - expected_si

    result = calculate_stability_measure(df)

    assert result["STA"] == pytest.approx(expected_sta)
    assert result["sr"] == pytest.approx(expected_sr)
    assert result["si"] == pytest.approx(expected_si)
