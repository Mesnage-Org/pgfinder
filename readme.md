# pgfinder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/Mass-Spec-pgfinder-Analysis/jupyter?filepath=pgfinder-demo.ipynb)
## Installation

Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) (it also works with [anaconda](https://docs.anaconda.com/anaconda/install/), but we do not need the extra packages). With conda installed, run the following commands to create the virtual environment and activate it:

```
conda env create -f environment.yml
conda activate pgfinder
```
## Usage

```
python demo.py
```

## Testing

To run tests:

```
pytest
```

The tests check output against an [expected baseline](data/baseline_output.csv). To recreate this (e.g. in response to improvements to the scientific "correctness" of the code ouput), use:

```
python make_baseline.py
```

and replace the exisiting file.

**This software is licensed as specified by the [GPL License](COPYING) and [LGPL License](COPYING.LESSER).**