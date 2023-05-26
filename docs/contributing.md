# Contributing

There are a few ways to contribute:

- [Raise an issue](https://github.com/Mesnage-Org/pgfinder/issues) to identify a bug or suggest a new feature.
- Fork the repository and make a pull request to suggest changes to the code.
- If you'd like to contribute a mass database, please do this by [raising an
  issue](https://github.com/Mesnage-Org/pgfinder/issues).

## Development Installation

The current version when installed from GitHub is a combination of the most recent Git tag combined with the hash of the
current `HEAD` of the branch and how many commits away from the last tag it is. For further details on versioning please
refer to [versioneer documentation](https://github.com/python-versioneer/python-versioneer).

If you wish to contribute to the development of PGFinder you should clone (your fork of) this repository and install it
in editable mode (`pip install -e`) with the following commands which install additional dependencies for tests,
documentation and linting.

```bash
# Clone the repository
git clone https://github.com/Mesnage-Org/PGFinder.git
cd pgfinder
# Install in editable mode
pip install -e .
# Install extra dependencies
pip install -e ".[dev,docs,tests]"
```

## Testing

To run unit tests suite use [pytest](https://pytest.org)

```bash
pytest
```

## Linting

PGFinder uses [pre-commit](https://pre-commit.com) hooks to ensure code conforms to the [PEP8 Python Style
Guide](https://pep8.org/) using the [ruff](https://duckduckgo.com/?q=ruff+linter&t=opera&ia=images) linter, applies
[black](https://black.readthedocs.io/en/stable/index.html) formatting and ensures Notebooks are clean on
submission. These hooks are run on GitHub when Pull Requests are made using [pre-commit.ci](https://pre-commit.ci) and
if you have not run them locally then your pull request will fail the tests it needs to pass.

`pre-commit` will have been installed as part of the extra dependencies above (they are part of `dev`), but you need to
install `pre-commit` and the hooks locally in your virtual environment. This can be done with the following commands.

``` bash
pre-commit install
pre-commit install-hooks
```

Now when you make a `git commit` the hooks will run first and report any errors. Sometimes if the errors can be
corrected automatically they will be and the files will be modified in place, but you will have to then `git stage` the
modified files again before completing the commit (this gives you an opportunity to review the changes that have been
made but typically they are ok to accept, they will be `black` formatting or Notebook cleaning).


## Releasing to PyPI

Release to the [Python Package Index (PyPI)](https://pypi.org) are automated and occur when a new release is made on
GitHub with a tag that begins with `v#.#.#'`. PGFinder uses [semantic verisoning](https://semver.org/).

### Pre-release candidates

If you have new features you wish to test using the [PGFinder JupyterLite
Notebook](https://github.com/Mesnage-Org/pgfinder-jupyterlite) then the tag should indicate that this is a "pre-release"
and as well as a semantic release number it should be followed with one of the [PEP0440 pre-release
spellings](https://peps.python.org/pep-0440/#pre-release-spelling) (using a [pre-release
separator](https://peps.python.org/pep-0440/#pre-release-separators)). For example if the most recent release is
`v0.0.4` and you have a new feature you wish to test in the Jupyter Lite Notebook the tag should take the form
`v0.0.4-a1` to indicate this is the first alpha revision of the new feature. If you find errors and correct them bump
the number following `a` i.e. `v0.0.4-a2`. Once you are happy that the new feature is working as desired you can proceed
with making a new release which in this example, following semantic versioning, would be `v0.0.5`.
