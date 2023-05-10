# Contributing

There are a few ways to contribute:

- [Raise an issue](https://github.com/Mesnage-Org/pgfinder/issues) to identify a bug or suggest a new feature.
- Fork the repository and make a pull request to suggest changes to the code.
- If you'd like to contribute a mass database, please do this by [raising an issue](https://github.com/Mesnage-Org/pgfinder/issues).

## Development Installation

The current version when installed from GitHub is a combination of the most recent Git tag combined with the hash of the
current `HEAD` of the branch and how many commits away from the last tag it is. For further details on versioning please
refer to [versioneer documentation](https://github.com/python-versioneer/python-versioneer).

If you wish to contribute to the development of PGFinder you should clone (your fork of) this repository and install it in editable
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

## Testing

To run unit tests:

```bash
pytest
```

The tests check output against an expected baseline for [Maxquant](data/baseline_output.csv) or
[FTRS](data/baseline_output_ftrs.csv). To recreate this (e.g. in response to improvements to the scientific
"correctness" of the code ouput), use:


```bash
python make_baseline.py
```

...and replace the existing file.