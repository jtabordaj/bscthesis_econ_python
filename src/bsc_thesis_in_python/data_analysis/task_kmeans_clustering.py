import os
import warnings
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
warnings.filterwarnings("ignore")

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Polygon as MplPolygon
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from bsc_thesis_in_python.config import BLD, DOCUMENTS

FEATURES = ["CON", "STA", "TO"]
COLORS = ["#ec1010", "#2E9FDF"]


def standardize_data(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """Standardize features using Sample Standard Deviation (N-1).

    Args:
        df (pd.DataFrame): Input DataFrame.
        features (list[str]): List of column names to scale.

    Returns:
        pd.DataFrame: DataFrame of standardized features with original indices.
    """
    return (df[features] - df[features].mean()) / df[features].std()


def perform_kmeans(
    x_scaled: pd.DataFrame, n_clusters: int = 2, random_state: int = 55
) -> np.ndarray:
    """Run K-Means clustering algorithm.

    Args:
        x_scaled (pd.DataFrame): Standardized DataFrame.
        n_clusters (int): Number of clusters (k), defaults to 2.
        random_state (int): Seed for reproducibility.

    Returns:
        np.ndarray: A NumPy Array of cluster labels.
    """
    kmeans = KMeans(
        n_clusters=n_clusters,
        n_init=10,
        random_state=random_state,
        algorithm="lloyd",
    )
    return kmeans.fit_predict(x_scaled)


def perform_pca_reduction(x_scaled: pd.DataFrame, n_components: int = 2):
    """Reduce dimensions to 2D using PCA for visualization.

    Args:
        x_scaled (pd.DataFrame): Standardized data array.
        n_components (int): Number of components to keep.

    Returns:
        tuple[pd.DataFrame, PCA]: Tuple of (two-component dataframe, fitted PCA object).
    """
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(x_scaled)

    pca_df = pd.DataFrame(data=principal_components, columns=["PC1", "PC2"])
    return pca_df, pca


def plot_clusters(
    pca_df: pd.DataFrame, explained_variance, labels, save_path: Path
) -> None:
    """Generate and save the PCA cluster plot with Convex Hulls (Polygons).

    Args:
        pca_df (pd.DataFrame): DataFrame with PC1, PC2 columns and Cluster labels.
        explained_variance (np.ndarray): Array of variance ratios for axis labels.
        labels (pd.Series): List of text labels (CIIU4) for the points.
        save_path (Path): Path to save the PNG file.
    """
    plt.figure(figsize=(12, 8))

    sns.scatterplot(
        x="PC1",
        y="PC2",
        hue="Cluster",
        palette=COLORS,
        data=pca_df,
        s=100,
        alpha=0.8,
        edgecolor="black",
    )

    for cluster_id, color in zip(sorted(pca_df.Cluster.unique()), COLORS):
        cluster_points = pca_df[pca_df.Cluster == cluster_id][["PC1", "PC2"]].values
        if len(cluster_points) >= 3:
            hull = ConvexHull(cluster_points)
            hull_points = cluster_points[hull.vertices]
            poly = MplPolygon(
                hull_points,
                closed=True,
                facecolor=color,
                alpha=0.15,
                edgecolor=color,
                linewidth=2,
            )
            plt.gca().add_patch(poly)

    for i in range(pca_df.shape[0]):
        plt.text(
            x=pca_df.PC1[i] + 0.05,
            y=pca_df.PC2[i] + 0.05,
            s=labels[i],
            fontdict=dict(color="black", size=9),
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=0.5),
        )

    plt.title(
        "Characterization of Colombian Manufacture using a two groups k-means clustering method",
        fontsize=14,
    )
    plt.xlabel(f"Dim1 ({explained_variance[0]:.1%})", fontsize=12)
    plt.ylabel(f"Dim2 ({explained_variance[1]:.1%})", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(title="cluster")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def task_perform_clustering(
    depends_on: Path = BLD / "industry_measures.csv",
    produces: dict[str, Path] = {
        "plot_path": DOCUMENTS / "public" / "kmeans_cluster_plot.png",
        "data_path": BLD / "kmeans_cluster.csv",
    },
) -> None:
    """Orchestrate the K-Means clustering analysis pipeline.

    This task reads a frame of industry measures (.csv), applies
    mean standardization, kmeans clusterization and principal component
    analysis, returns a file with kmeans predictions (.csv) and a plot of
    the cluster (.png).
    """
    df = pd.read_csv(depends_on)
    
    x_scaled = standardize_data(df, FEATURES)

    clusters = perform_kmeans(x_scaled)

    pca_df, pca_model = perform_pca_reduction(x_scaled)

    pca_df["PC1"] = -pca_df["PC1"]
    
    pca_df["Cluster"] = clusters + 1
    df["Cluster"] = clusters + 1

    plot_clusters(
        pca_df=pca_df,
        explained_variance=pca_model.explained_variance_ratio_,
        labels=df["CIIU4"],
        save_path=produces["plot_path"],
    )

    output_columns = ["CIIU4", "STA", "CON", "TO", "Cluster"]
    df[output_columns].to_csv(produces["data_path"], index=False)


if __name__ == "__main__":
    task_perform_clustering()
