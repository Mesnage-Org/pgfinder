"""Test pgio functions."""
from pathlib import Path
from unittest import TestCase

import pandas as pd

from pgfinder.gui.internal import ms_upload_reader, theo_masses_upload_reader
from pgfinder.pgio import ms_file_reader, read_yaml

BASE_DIR = Path.cwd()
RESOURCES = BASE_DIR / "tests" / "resources"


def test_ms_file_reader(ftrs_file_name):
    assert isinstance(ms_file_reader(ftrs_file_name), pd.DataFrame)


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
