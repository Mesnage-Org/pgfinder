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

### GitHub

If you do not intend to undertake any development on PGFinder and just wish to use it then you can install directly from
the GitHub repository using `pip` under the virtual environment. The first method leverages `pip`'s ability to install
directly from GitHub...

```bash
pip install git+https://github.com/Mesnage-Org/PGFinder.git
```

Alternatively you can clone the repository and then install it...

``` bash
git clone git@github.com:Mesnage-Org/pgfinder.git
cd pgfinder
pip install .
```


## Binder Notebooks

Interactive notebooks are available for different versions from the links below. For descriptions of the features of each version
please refer to the [Releases](https://github.com/Mesnage-Org/pgfinder/releases) page. If you wish to use the latest changes
and improvements select the Notebooks from the `current` version which reflects changes made to the `master` branch that
have not yet been released.

| Version  | Interactive | Example |
|----------|-------------|---------|
| `current` | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder_interactive.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder.ipynb) |
| `v0.1.0` | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/v0.1.0?urlpath=tree/pgfinder_interactive.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/v0.1.0?urlpath=tree/pgfinder.ipynb) |


## Data Dictionary

The project [data dictionary](data_dictionary.md).

### Development

If you wish to contribute to the development of PGFinder you should clone this repository and install it in editable
mode (`pip install -e`) with the following commands.


```bash
# Clone the repository
git clone https://github.com/Mesnage-Org/PGFinder.git
cd pgfinder
# Install in editable mode
pip install -e .
# Install test dependencies
pip install -e .[tests]
```
