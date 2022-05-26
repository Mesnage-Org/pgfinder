# Usage

A demo is available with...

```bash
python demo.py
```

You can also use the command line interface `find_pg.py` which works with a YAML configuration file (see
`config/example.yaml`) for an example which you can modify. You must supply at least one option on the command line `-c
<path/to/config.yaml>`, so to use the example config you would.

``` bash
./find_pg -c config/example.yaml
```

Each option in the configuration file can be over-ridden at the command line, see `pythong find_pg.py --help** for more
information.

**FIXME** Need to make this work on M$-Windows as easily as possible, ideally avoiding the need for users to install
virtual environments such as [Miniconda](https://docs.conda.io/en/latest/miniconda.html), to which end investigate
packaging with [pipx](https://pypa.github.io/pipx/), although if the plan long-term is to develop a WebUI/service should
time be spent on this?

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
