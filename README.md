# PGFinder

![CI Tests](https://github.com/Mesnage-Org/pgfinder/actions/workflows/ci-tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/Mesnage-Org/pgfinder/branch/master/graph/badge.svg?token=5SM94G9Z6K)](https://codecov.io/gh/Mesnage-Org/pgfinder)
[![PyPI version](https://img.shields.io/pypi/v/pgfinder?color=blue)](https://pypi.org/project/pgfinder/)
[![Docs](https://img.shields.io/badge/github.io-docs-green)](https://mesnage-org.github.io/pgfinder/)
[![](https://img.shields.io/badge/ORDA--DOI-10.15131%2Fshef.data.20101751.v1-lightgrey)](https://doi.org/10.15131/shef.data.20101751.v1)

A web-site for processing samples is available at [PGFinder](https://mesnage-org.github.io/pgfinder-gui/). For
descriptions of the features of each version please refer to the
[Releases](https://github.com/Mesnage-Org/pgfinder/releases) page. If you wish to use the development version please
refer to the [Installation](https://mesnage-org.github.io/pgfinder/master/installation.html) and
[Usage](https://mesnage-org.github.io/pgfinder/master/usage.html) documentation.

For an introduction to Peptidoglycan analysis please refer to the
[documentation](https://mesnage-org.github.io/pgfinder/master/introduction.html).

## Usage

PGFinder is available in two forms a web-based User Interface (WebUI) at
[mesnage-org.github.io/pgfinder-gui/](https://mesnage-org.github.io/pgfinder-gui/) or a command line interface (CLI)
Python package.


Thecommand-line programme (`find_pg`) uses a YAML configuration file as input.

``` bash
find_pg -c config.yaml
```

For details of using the CLI version including the configuration file please refer to the
[Usage](https://mesnage-org.github.io/pgfinder/master/usage.html) section of the Documentation.

## Installation

Detailed installation instructions can be found in the
[Installation](https://mesnage-org.github.io/pgfinder/master/installation.html) section of the Documentation.

PGFinder is available from [PyPI](https://pypi.org/project/pgfinder/) so can be installed with `pip`.

``` bash
pip install pgfinder
```

It can also be installed directly from this repository

``` bash
pip install git+https://github.com/Mesnage-Org/PGFinder.git
```

Or you can clone the repository and install it.

``` bash
git clone https://github.com/Mesnage-Org/pgfinder.git
cd pgfinder
pip install -e .
```

## Contributing

Contributions are welcome, please refer to the detailed
[Contributing](https://mesnage-org.github.io/pgfinder/master/contributing.html) section of the Documentation which
details how to setup and install all components and setup/configure the development tools such as `pre-commit`.

## Copying

This software is licensed as specified by the GPL License and LGPL License. Please refer to the
[`COPYING`](https://github.com/Mesnage-Org/pgfinder/blob/master/COPYING) and
[COPYING.LESSER](https://github.com/Mesnage-Org/pgfinder/blob/master/COPYING.LESSER) files for further details.

## Links

* [Mesnage Lab](https://mesnagelab.weebly.com/)
* [PGFinder On-Line](https://mesnage-org.github.io/pgfinder-gui/)

## References

* [PGFinder, a novel analysis pipeline for the consistent, reproducible, and high-resolution structural analysis of bacterial peptidoglycans | eLife](https://elifesciences.org/articles/70597)
