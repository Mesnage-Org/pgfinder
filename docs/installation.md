# Installing PGFinder

## Virtual Environment

Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) (it also works with
[anaconda](https://docs.anaconda.com/anaconda/install/), but we do not need the extra packages). With Conda installed,
run the following commands to create the virtual environment and activate it:


```bash
conda create --force -n pgfinder python=3.7
conda activate pgfinder
```

You're fine to use a different virtual environment, if you want!

## PyPI

`PGFinder` is available via the [Python Package Index (PyPI)](https://pypi.org/) and the latest release can be installed
under your virtual environment with [`pip`](https://pip.pypa.io/en/stable/).

``` bash
pip install pgfinder
```

Versions are released automatically when commits on GitHub are tagged.

To install the most recent pre-release version, use:

``` bash
pip install git+https://github.com/Mesnage-Org/PGFinder.git
```

Developers should follow the [developer installation instructions](contributing.md).

## Binder Notebooks

[Online, interactive notebooks are available for different versions of pgfinder](usage.md). 

To install these locally, use:

``` bash
pip install pgfinder[notebooks]
```

*This command does not currently work and will be enabled in a later version.*
