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

If you do not intend to undertake any development on pgfinder and just wish to use it then you can install directly from
the GitHub repository using `pip` under the virtual environment.

```bash
pip install git+https://github.com/Mesnage-Org/PGFinder.git
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
