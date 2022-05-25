# Installing pgfinder

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

A release to the [PyPi](https://pypi.org/) is planned which will make it possible to install pgFinder using
[`pip`](https://pip.pypa.io/en/stable/).

``` bash
pip install pgfinder
```

For now though you will have to install the package from this Git repository.

### GitHub

If you do not intend to undertake any development on pgfinder and just wish to use it then you can install directly from
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


## Data Dictionary

The project [data dictionary](data_dictionary.md).

### Development

If you wish to contribute to the development of pgfinder you should clone this repository and install it in editable
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
