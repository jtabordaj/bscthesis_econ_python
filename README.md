[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/i9Zy4NKR)

# From R to Python: Replication of my Bachelor Thesis in Economics.

This document reports a Python implementation of the data pipeline and analysis I
originally developed in R for my Bachelor Thesis. The project replicates the
construction of literature-inspired Schumpeterian innovation indices (Concentration,
Stability, and Technological Opportunities) and the K-Means clustering analysis for
Colombian manufacturing industries. The workflow is managed by `pytask` to ensure full
reproducibility, with `pytest` testing for each of the measures.

## Pre-Requirements

On top of the usual [Git](https://git-scm.com/install/) and
[Visual Studio](https://code.visualstudio.com/download) tuple, to run this project you
should have installed:

1. The package management program [pixi](https://pixi.prefix.dev/latest/#installation).
1. A LaTeX engine such as [MikTex](https://miktex.org/).
1. A `perl` environment such as [Strawberry Perl](https://strawberryperl.com/).

## Cloning and Installing in local

To obtain a copy of the project locally, open a `cmd` in your desired folder route and
type:

```
git clone "https://github.com/iame-uni-bonn/final-project-jtabordaj"
```

This will allow you to open the folder in an IDE such as Visual Studio for the next
steps. Alternatively, you can keep working in `cmd`. To install the project dependencies
and pre-commit hooks for eventual version control, type the following commands:

```
pixi run prek install
pixi install
```

This process might take a while during the first run. But once done you are good to go.

## Running the project

In order to get all the calculations, plots and documents for this project, make use of
the following command:

```
pixi run pytask
```

If you are interested in unit testing for this project, you can make use of:

```
pixi run pytest -v
```

All the results of `pytask` and `pytest` will print to console, you can find
intermediate files in `bld` for manual auditing. Moreover, if you want to read a small
report on the project, you can make use of:

```
pixi run view-paper
```

This will open a `localhost` port in your computer.
