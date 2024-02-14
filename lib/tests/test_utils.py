"""Test utils."""

from decimal import Decimal
from pathlib import Path

from pgfinder.utils import convert_path, dict_to_decimal, update_config


def test_convert_path(tmpdir) -> None:
    """Test path conversion."""
    test_dir = str(tmpdir)
    converted_path = convert_path(test_dir)

    assert isinstance(converted_path, Path)
    assert tmpdir == converted_path


def test_update_config() -> None:
    """Test updating configuration."""
    SAMPLE_CONFIG = {"input_file": "there", "masses_file": "something", "output_dir": "here"}
    NEW_VALUES = {"output_dir": "something new"}
    updated_config = update_config(SAMPLE_CONFIG, NEW_VALUES)

    assert isinstance(updated_config, dict)
    assert updated_config["output_dir"] == Path("something new")


def test_dict_to_decimal() -> None:
    """Test conversion of floats to decimal."""
    SAMPLE_DICT = {"a": 164.1234, "b": {"c": 987.6543}, "d": "a string"}

    decimal_dict = dict_to_decimal(SAMPLE_DICT)

    assert isinstance(decimal_dict, dict)
    assert isinstance(decimal_dict["a"], Decimal)
    assert isinstance(decimal_dict["b"]["c"], Decimal)
    assert isinstance(decimal_dict["d"], str)
