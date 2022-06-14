# Usage

There are two approaches to using PGFinder, Notebooks or at the Command Line.

## Notebooks

Online Binder Notebooks are provided for use at the following locations.

Interactive notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder_interactive.ipynb)

Example notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Mesnage-Org/PGFinder/master?urlpath=tree/pgfinder.ipynb)

## Command Line

If you wish to use the command line version you will have to follow the [installation](installation.md) instructions to
install PGFinder on your computer. Once you have done so a demo is available with...

```bash
python demo.py
```

## `find_pg`

You can also use the command line interface `find_pg` which works with a YAML configuration file (see
`config/example.yaml`) for an example which you can modify. You must supply at least one option on the command line `-c
<path/to/config.yaml>`, so to use the example config you would.

``` bash
find_pg -c config/example.yaml
```

Each option in the configuration file can be over-ridden at the command line, see `pythong find_pg.py --help** for more
information.


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
