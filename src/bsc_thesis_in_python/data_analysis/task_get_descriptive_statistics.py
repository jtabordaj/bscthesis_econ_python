import pandas as pd
from pathlib import Path
from scipy.stats import kurtosis, skew

from bsc_thesis_in_python.config import BLD

TARGET_FEATURES = ["STA", "CON", "TO"]

def compute_statistics(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """Calculate basic and advanced statistics for the k-means cluster results.

    Args:
        df (pd.DataFrame): A dataframe with the k-means cluster result.
        features (list[str]): A list with the features to calculate over.

    Returns:
        pd.DataFrame: A DataFrame where the index is the feature name and columns 
        are the computed statistics.
    """
    subset = df[features]
    
    basic_stats = subset.agg(["max", "min", "mean", "std"]).transpose()

    advanced_stats = subset.agg([
        lambda x: kurtosis(x, nan_policy="omit"),
        lambda x: skew(x, nan_policy="omit")
    ])
    
    advanced_stats.index = ["kurtosis", "skewness"]
    advanced_stats = advanced_stats.transpose()

    return pd.concat([basic_stats, advanced_stats], axis=1)


def task_compute_cluster_statistics(
    depends_on: Path = BLD / "kmeans_cluster.csv",
    produces: dict[str, Path] = {
        "cluster_1_stats": BLD / "descriptives_cluster_1.csv",
        "cluster_2_stats": BLD / "descriptives_cluster_2.csv",
    },
) -> None:
    """Orchestrate the K-Means clustering descriptive analysis.

    This task reads the kmeans output dataset (.csv) and calculates the mean,
    min, max, standard deviation, kurtosis and skewness. It returns two
    dataframes (.csv), one for each cluster.
    """
    df = pd.read_csv(depends_on)
    
    df_c1 = df[df["Cluster"] == 1]
    df_c2 = df[df["Cluster"] == 2]
    
    stats_c1 = compute_statistics(df_c1, TARGET_FEATURES)
    stats_c2 = compute_statistics(df_c2, TARGET_FEATURES)
    
    stats_c1.to_csv(produces["cluster_1_stats"])
    stats_c2.to_csv(produces["cluster_2_stats"])


if __name__ == "__main__":
    task_compute_cluster_statistics()
