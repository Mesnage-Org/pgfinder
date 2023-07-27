"""Test pgio functions."""
from pathlib import Path
from unittest import TestCase

import pandas as pd

# FIXME: Don't let this stick around!
from pgfinder.pgio import (
    long_to_wide,
    ms_upload_reader,
    read_yaml,
    theo_masses_upload_reader,
)

BASE_DIR = Path.cwd()
RESOURCES = BASE_DIR / "tests" / "resources"


def test_ms_upload_reader(ipywidgets_upload_output):
    assert isinstance(ms_upload_reader(ipywidgets_upload_output), pd.DataFrame)


def test_theo_masses_upload_reader(ipywidgets_upload_output_theo):
    assert isinstance(theo_masses_upload_reader(ipywidgets_upload_output_theo), pd.DataFrame)


CONFIG = {
    "this": "is",
    "a": "test",
    "yaml": "file",
    "numbers": 123,
    "logical": True,
    "nested": {"something": "else"},
    "a_list": [1, 2, 3],
}


def test_read_yaml() -> None:
    """Test reading of YAML file."""
    sample_config = read_yaml(RESOURCES / "test.yaml")

    TestCase().assertDictEqual(sample_config, CONFIG)


def test_long_to_wide() -> None:
    """Test conversion of wide to long format."""
    long_df = pd.read_csv(RESOURCES / "long_results.csv")
    wide_df = pd.read_csv(RESOURCES / "wide_results.csv")

    reshaped_long_df = long_to_wide(long_df)

    pd.testing.assert_frame_equal(reshaped_long_df, wide_df, check_dtype=False)
