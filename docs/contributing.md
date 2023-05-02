# Contributing

There are a few ways to contribute:

- [Raise an issue](https://github.com/Mesnage-Org/pgfinder/issues) to identify a bug or suggest a new feature.
- Fork the repository and make a pull request to suggest changes to the code.
- If you'd like to contribute a mass database, please do this by [raising an issue](https://github.com/Mesnage-Org/pgfinder/issues).

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