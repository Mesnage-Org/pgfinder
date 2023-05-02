# Contributing

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