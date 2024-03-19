"""Test pgio functions."""

from pathlib import Path
from unittest import TestCase

import pandas as pd

from pgfinder import pgio
from pgfinder.gui.internal import ms_upload_reader, theo_masses_upload_reader

BASE_DIR = Path.cwd()
RESOURCES = BASE_DIR / "tests" / "resources"


def test_ms_file_reader_ftrs(ftrs_file_name):
    """Test Mass Spectrometer file reader with ftrs 311 and 52 file formats."""
    assert isinstance(pgio.ms_file_reader(ftrs_file_name), pd.DataFrame)


def test_ms_file_reader_maxquant(mq_file_name):
    """Test Mass Spectrometer file reader with maxuant formats."""
    assert isinstance(pgio.ms_file_reader(mq_file_name), pd.DataFrame)


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
    sample_config = pgio.read_yaml(RESOURCES / "test.yaml")

    TestCase().assertDictEqual(sample_config, CONFIG)
