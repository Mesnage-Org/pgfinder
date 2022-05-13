# pgfinder

![CI Tests](https://github.com/Mesnage-Org/pgfinder/actions/workflows/ci-tests.yml/badge.svg) [![codecov](https://codecov.io/gh/Mesnage-Org/pgfinder/branch/master/graph/badge.svg?token=5SM94G9Z6K)](https://codecov.io/gh/Mesnage-Org/pgfinder)

Interactive notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder_interactive.ipynb)

Example notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder.ipynb)

## Installation

Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) (it also works with [anaconda](https://docs.anaconda.com/anaconda/install/), but we do not need the extra packages). With conda installed, run the following commands to create the virtual environment and activate it:

```
conda create --force -n pgfinder python=3.7
conda activate pgfinder
```

### Normal Use

```
pip install git+https://github.com/Mesnage-Org/PGFinder.git
```

## Data Dictionary

The project [data dictionary](data_dictionary.md).

### Development

Clone this repository:

```bash
git clone https://github.com/Mesnage-Org/PGFinder.git
cd pgfinder
```

Install for development:

```bash
pip install -e .
```

You're fine to use a different virtual environment, if you want!

## Usage

A demo is available with...

```bash
python demo.py
```

You can also use the command line interface `find_pg.py` which works with a YAML configuration file (see
`config/example.yaml`) for an example which you can modify. You must supply at least one option on the command line `-c
<path/to/config.yaml>`, so to use the example config you would.

``` bash
python find_pg.py -c config/example.py
```

Each option in the configuration file can be over-ridden at the command line, see `pythong find_pg.py --help` for more information.

## Testing

To run tests:

```bash
pytest
```

The tests check output against an expected baseline for [Maxquant](data/baseline_output.csv) or [FTRS](data/baseline_output_ftrs.csv). To recreate this (e.g. in response to improvements to the scientific "correctness" of the code ouput), use:

```bash
python make_baseline.py
```

and replace the existing file.

**This software is licensed as specified by the [GPL License](COPYING) and [LGPL License](COPYING.LESSER).**
