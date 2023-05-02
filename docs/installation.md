# Installing PGFinder

Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) (it also works with
[anaconda](https://docs.anaconda.com/anaconda/install/), but we do not need the extra packages). With Conda installed,
run the following commands to create the virtual environment and activate it:


```bash
conda create --force -n pgfinder python=3.7
conda activate pgfinder
```

You're fine to use a different virtual environment, if you want!


## Normal Use

### PyPi

`PGFinder` is available via the [Python Package Index (PyPi)](https://pypi.org/) and the latest release can be installed
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

Interactive notebooks are available for different versions from the links below. For descriptions of the features of each version
please refer to the [Releases](https://github.com/Mesnage-Org/pgfinder/releases) page. If you wish to use the latest changes
and improvements select the Notebooks from the `current` version which reflects changes made to the `master` branch that
have not yet been released.

| Version  | Interactive | Example |
|----------|-------------|---------|
| `current` | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder_interactive.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder.ipynb) |
| `v0.1.0` | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/v0.1.0?urlpath=tree/pgfinder_interactive.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/v0.1.0?urlpath=tree/pgfinder.ipynb) |
