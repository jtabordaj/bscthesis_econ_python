# Replication Report: A Characterization of Colombian Industries under Schumpeter's Patterns of Innovation

+++ {"part": "Summary"}

This document reports a Python implementation of the data pipeline and analysis I
originally developed in R for my Bachelor Thesis {cite}`Taborda2022`. The project
replicates the construction of literature-inspired Schumpeterian innovation indices
(Concentration, Stability, and Technological Opportunities) and the K-Means clustering
analysis for Colombian manufacturing industries. The workflow is managed by `pytask` to
ensure full reproducibility, with `pytest` testing for each of the measures.

+++

```{raw} latex
\clearpage
```

# Introduction

In {cite}`Taborda2022` (my Bachelor Thesis), I characterized Colombian industries under
Joseph Schumpeter's Mark I and Mark II patterns of innovation. That original study,
conducted in R, utilized a complex merging of the Annual Manufacturing Survey (EAM) and
the Survey of Development and Technological Innovation (EDIT), both produced and
maintained by DANE (Colombia's National Department of Statistics).

This project ports that quantitative workflow to Python using
{cite}`GaudeckerEconProjectTemplates`. project template, leveraging modern data
management tools to ensure reproducibility. The goal is to arrive at the clustering
results which identified two distinct groups of industries based on market structure,
and do so using a robust, DAG-based pipeline.

# Methodology

Following the original methodology, I construct three primary economic indices for each
industry $j$ (CIIU4 classification) based on the merged microdata from 2017-2018:
Concentration, Stability, Technological Opportunities.

Concentration Index (CON) replicates the geometric mean of Herfindahl-Hirschman Indices
(HHI) across four dimensions: market share ($MS$), innovation share ($MSA$), labor share
($LDS$), and supply share ($SS$). This measures the dominance of incumbent firms.

$ CON_j = (HHI_{MS} \times HHI_{MSA} \times HHI_{LDS} \times HHI_{SS})^{0.25} $.

Stability Index (STA) captures the dynamic of innovation leadership by comparing the
share of radical ($sr$) versus incremental ($si$) innovations.

$ STA_j = sr_j - si_j $.

Finally, Technological Opportunities (TO) measures the status of the appropriability regime using the
ratio of new protection mechanisms registered to the industry total of existing mechanisms available.

$ TO_j = \frac{\sum PM_{1718} + \sum NCPM_{1718}}{\sum PM_{total}} $.

These variables are used to construct a two-group k-means cluster algorithm. However the path from building the measures to obtaining the cluster is not straightforward, as there are some techniques in between.

To begin with, data undergoes Standardization and Distance Normalization processing. This is done to address the "distance sensitivity" problem inherent in Euclidean distance calculations. The dataset includes variables with vastly different magnitudes—such as small percentage points for innovation versus millions of pesos for sales. If left raw, the larger values would dominate the distance metric. To fix this, the study uses Sample Deviation Standardization (N-1) to normalize the vectors. Consequently, the Euclidean distances calculated during clustering are measured in units of standard deviations. 

Once that is done, in order to obtain the visualization of the clusters, there must be a dimensionality reduction technique. The k-means implementation here employs Principal Component Analysis (PCA) to project the multi-dimensional data onto a 2D plane.  The resulting axes capture the maximum variance from the original dataset. In this specific analysis. 

Finally, the algorithm at its core uses Lloyd's Algorithm set to identify 2 groups ($k=2$). The process follows an iterative cycle: Each industry is assigned to the cluster whose centroid (mean) is closest by standardized Euclidean distance, then the centroid of each group is recalculated to be the exact mean of the data points currently assigned to it until the assignments stabilize and data points no longer switch groups.

# Results

The Python pipeline reproduces the K-Means clustering algorithm ($k=2$) used in the
original thesis to a degree of similarity. The standardization and Principal Component
Analysis (PCA) steps yield {ref}`fig:cluster`.

```{figure} public/kmeans_cluster_plot.png
---
width: 85%
label: fig:cluster
---
K-Mean cluster of Colombian Manufacturing Industries.
```

{ref}`fig:cluster` replicates the separation of industries into two distinct
groups, consistent with the original findings (compare with Figure 1 in {cite}`Taborda2022`). However, it will not be entirely similar to the original k-means as this machine
learning technique carries a non-deterministic component.

# Code Logic

## Template

This project does not depart from scratch. It borrows (most of) the template proposed by
{cite}`GaudeckerEconProjectTemplates` for Programming in Economics, enhanced by
`pytask`, `pytest` and running on `pixi` package management tool.

## Required packages

While `pixi` manages package and dependencies for you, a (non exhaustive) list of important dependencies for this project can be found below.

- pandas (Data manipulation and analysis)
- numpy (Numerical computing)
- scipy (Scientific computing, specifically stats and spatial)
- scikit-learn (Machine learning, imported as sklearn for K-Means and PCA)
- matplotlib (Plotting and visualization)
- seaborn (Statistical data visualization)
- pyreadstat (Reading SAS/SPSS/Stata .dta files)
- pyarrow (Required for reading/writing .feather files)
- openpyxl (Required for reading/writing Excel .xlsx files)

## `data_management`

Data management is the first step in this project. It departs from a zipped file that
comes directly from DANE's database and must arrive at a final, industry-separated excel
file that serves as the base for the `data_analysis` section. This is done through a
series of tasks:

- `task_unzip_data.py`: This small task unzips the `.zip` folder from DANE into two
  `.dta` files, one for each survey.
- `task_read_prepare_surveys.py`: This task manages the loading, processing and renaming
  of variables within the `.dta` survey files.
- `task_merge_surveys.py`: This task merges both surveys into a unified file. Here is
  where `test_merge_surveys_sample_size.py` tests if the sample size corresponds what
  was expected.
- `task_merge_surveys.py`: This task reduces the merged dataset to 'necessary only'
  columns and discards everything else.
- `task_filter_merged_datasets.py`: This task reduces the merged dataset to 'necessary
  only' columns and discards everything else.
- `task_separate_industries.py`: This task splits the merged datasets into separate
  self-containing dataframes, where each holds the information of exactly one CIIU4
  industry. This is the starting point of `data_analysis`.

## `data_analysis`

Data analysis departs from the aforementioned task product and arrives at a kmeans
cluster plot and `.csv` file. This is done in four steps:

- `task_build_submeasures.py`: This task builds the submeasures of the research. These are variables at the firm-level that do not carry on to the analysis part by themselves but used to calculate other advanced measures.
- `task_build_measures.py`: This task constructs the signature STA, CON and TO measures of the research, based on the Methodology section.
- `task_kmeans_clustering.py`: This task calculates a 2-group k-means clustering as in the original paper. This is what produces {ref}`fig:cluster`.
- `task_get_descriptive_statistics`: This task calculates descriptive statistics of both groups, such as Max, Min, Mean, St. Dev, Kurtosis and Skewness.

## Testing

As an addition to the original R script. This template allows for testing if the sample
size obtained in this replication equals the original sample size, or if corner cases of
each measure behave as expected. This is done thoroughly across all the tasks found
inside the `./test` folder. A brief description for each task is found below:

- `test_merge_surveys_sample_size.py`: Asserts if the sample size obtained via Python
  equals the same size as the sample obtained in R after performing inner_joins.
- `test_build_measures_con.py`: Asserts if the CON measure (and its helper function for
  the HHI) behaves correctly for corner cases and randomly generated intermediate cases.
  For example: Monopoly, Perfect Competition and Intermediate Competition
- `test_build_measures_sta.py`: Asserts if the STA measure behaves correctly for corner
  cases and randomly generated intermediate cases. For example: Markets full of radical
  innovations, full of incremental innovations, and markets with both.
- `test_build_measures_to.py`: Asserts if the TO measure behaves correctly for corner
  cases and randomly generated intermediate cases. For example: Markets with no new
  protection mechanisms, markets with no protection mechanisms at all, and those with
  intermediate cases of appropriability.

# Limitations

Replicating K-means clustering results across different computing engines, such as R to Python working in different CPU cores, is fundamentally limited by the algorithm’s sensitivity to initialization. K-means is a non-convex optimization problem, meaning it converges to local rather than global optima. Even when using the same random seed across programs different, these often utilize different pseudo RNG's or initialization strategies. Consequently, even a microscopic difference in the starting coordinates causes the algorithm to diverge into different cluster assignments. 

On top of math limitations, equal results are hindered by non-associativity of floating-point arithmetic. Differences in hardware architecture across CPUs (See AMD versus Intel cores), compilers, and the influence of parallel processing means that operations occur in different orders across engines. These minute discrepancies in distance calculations accumulate during every iteration, eventually leading to edge-case data points shifting between clusters. 

To end with this section, K-means algorithms are essentially different solvers using different logic to swap points and minimize error. Additionally, internal convergence criteria—such as the tolerance threshold for stopping the algorithm—often vary by implementation. Therefore, unless one manually injects fixed centroid coordinates from a source model into the target engine, differences are to be expected.

```
```
