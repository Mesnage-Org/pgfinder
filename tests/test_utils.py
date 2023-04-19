"""Test utils."""
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd

from pgfinder.utils import convert_path, update_config, dict_to_decimal, calculate_ppm_delta


def test_convert_path(tmpdir) -> None:
    """Test path conversion."""
    test_dir = str(tmpdir)
    converted_path = convert_path(test_dir)

    assert isinstance(converted_path, Path)
    assert tmpdir == converted_path


def test_update_config(caplog) -> None:
    """Test updating configuration."""
    SAMPLE_CONFIG = {"input_file": "there", "masses_file": "something", "output_dir": "here"}
    NEW_VALUES = {"output_dir": "something new"}
    updated_config = update_config(SAMPLE_CONFIG, NEW_VALUES)

    assert isinstance(updated_config, dict)
    assert "Updated config config[output_dir] : here > something new" in caplog.text
    assert updated_config["output_dir"] == Path("something new")


def test_dict_to_decimal() -> None:
    """Test conversion of floats to decimal."""
    SAMPLE_DICT = {"a": 164.1234, "b": {"c": 987.6543}, "d": "a string"}

    decimal_dict = dict_to_decimal(SAMPLE_DICT)

    assert isinstance(decimal_dict, dict)
    assert isinstance(decimal_dict["a"], Decimal)
    assert isinstance(decimal_dict["b"]["c"], Decimal)
    assert isinstance(decimal_dict["d"], str)


def test_calculate_ppm_delta() -> None:
    """Test addition of PPM column."""
    SAMPLE_DF = pd.DataFrame({"obs": [5645.35435454, 1, 879546.3924093], "exp": [3954.49849514, 2, 879546.8974916]})
    DELTA_DF = pd.DataFrame({"diff_ppm": [427577.82345296827, -500000.0, -0.5742528357381609]})
    TARGET_DF = pd.concat([SAMPLE_DF, DELTA_DF], axis=1)

    pd.testing.assert_frame_equal(calculate_ppm_delta(SAMPLE_DF, observed="obs", theoretical="exp"), TARGET_DF)
