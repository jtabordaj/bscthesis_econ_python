import pandas as pd
import pytest

from bsc_thesis_in_python.config import BLD


def test_merge_datasets_sample_size():
    """
    Checks if the merged dataset is exactly the paper sample (6405 rows).

    This is a replication test. If it fails, the quantitative approach
    still works, but the sample selection will make it not match the
    original paper exactly.
    """
    file_path = BLD / "merged_data.feather"
    if not file_path.exists():
        pytest.skip("merged_data.feather not found. Have you tried 'pixi run pytask'?")

    df = pd.read_feather(BLD / "merged_data.feather")

    current_len = len(df)
    expected_len = 6405
    assert current_len == expected_len, (
        f"Warning: Expected 6405 rows, but found {current_len}. "
        "Sample deviates from original paper"
    )
