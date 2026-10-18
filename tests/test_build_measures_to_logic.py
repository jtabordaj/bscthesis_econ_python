import numpy as np
import pandas as pd

from src.bsc_thesis_in_python.data_analysis.task_build_measures import (
    calculate_technological_opportunities,
)


def test_to_zero_denominator_case():
    """
    Test the TO measure when the industry has no protection mechanisms.

    Test will pass if `calculate_technological_opportunities()` returns a 'TO'
    value of 0.
    """
    zeroappropriationmarket = np.zeros(20, dtype=int)

    df = pd.DataFrame(
        {
            "PM": zeroappropriationmarket,
            "PM1718": zeroappropriationmarket,
            "NCPM1718": zeroappropriationmarket,
        }
    )

    result = calculate_technological_opportunities(df)

    assert result["TO"] == 0.0


def test_to_stagnant_appropriation_case():
    """
    Test the TO measure when industry appropriation is stagnant.

    Test will pass if `calculate_technological_opportunities()` returns a 'TO'
    value of 0, but has valid registered protection mechanisms.
    """
    np.random.seed(58)  # noqa: NPY002
    zeroappropriationmarket = np.zeros(20, dtype=int)
    existingmechanismsmarket = np.random.randint(0, 100, 20)  # noqa: NPY002

    df = pd.DataFrame(
        {
            "PM": existingmechanismsmarket,
            "PM1718": zeroappropriationmarket,
            "NCPM1718": zeroappropriationmarket,
        }
    )

    result = calculate_technological_opportunities(df)

    assert result["TO"] == 0.0


def test_to_active_appropriation_case():
    """
    Test the TO measure when industry appropriation is active.

    Test will pass if `calculate_technological_opportunities()` returns a 'TO'
    value that is not zero 0.
    """
    np.random.seed(59)  # noqa: NPY002
    existingmechanismsmarket = np.random.randint(0, 100, 20)  # noqa: NPY002

    df = pd.DataFrame(
        {
            "PM": existingmechanismsmarket,
            "PM1718": existingmechanismsmarket,
            "NCPM1718": existingmechanismsmarket,
        }
    )

    result = calculate_technological_opportunities(df)

    assert result["TO"] != 0.0
