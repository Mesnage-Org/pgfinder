"""Test pgio functions."""

from pathlib import Path
from unittest import TestCase

import pandas as pd
import pytest

from pgfinder import pgio
from pgfinder.errors import UserError
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


@pytest.mark.parametrize(
    "content,message,cause",
    [
        pytest.param(b"", "mass database was empty", pd.errors.EmptyDataError, id="empty-file"),
        pytest.param(
            b'Structure,Monoisotopic Mass\n"gm-AE|1,500.0\n',
            "doesn't contain valid CSV",
            pd.errors.ParserError,
            id="unterminated-quote",
        ),
        pytest.param(
            b"Structure,Monoisotopic Mass\n\xff,500.0\n",
            "doesn't contain valid CSV",
            UnicodeDecodeError,
            id="invalid-utf8",
        ),
        pytest.param(
            b"Monoisotopic Mass\n500.0\n",
            "didn't have the correct columns",
            ValueError,
            id="missing-structure-column",
        ),
        pytest.param(
            b"Structure\ngm-AE|1\n",
            "didn't have the correct columns",
            ValueError,
            id="missing-mass-column",
        ),
    ],
)
def test_theo_masses_reader_invalid_csv(tmp_path, content, message, cause):
    """Translate parser errors into actionable user errors, preserving their causes."""
    file = tmp_path / "masses.csv"
    file.write_bytes(content)

    with pytest.raises(UserError, match=message) as exc_info:
        pgio.theo_masses_reader(file)

    assert isinstance(exc_info.value.__cause__, cause)


@pytest.mark.parametrize("structure", ["gm-AE", "gm-AE|", "gm-AE|two", "gm-AE|1extra"])
def test_theo_masses_reader_invalid_structure_suffix(tmp_path, structure):
    """One valid structure must not hide another structure's invalid suffix."""
    file = tmp_path / "masses.csv"
    file.write_text(f"Structure,Monoisotopic Mass\ngm-AE|1,500.0\n{structure},600.0\n", encoding="utf-8")

    with pytest.raises(UserError, match=r"structures missing the '\|n' suffix"):
        pgio.theo_masses_reader(file)


@pytest.mark.parametrize("path_type", [str, Path])
def test_theo_masses_reader_valid_structures(tmp_path, path_type):
    """Accept numeric suffixes and preserve the reader's columns and file metadata."""
    file = tmp_path / "masses.csv"
    file.write_text(
        "Monoisotopic Mass,Structure,Unused\n498.0,gm|0,a\n500.0,gm-AE|1,b\n600.0,gm-AE|12,c\n",
        encoding="utf-8",
    )

    result = pgio.theo_masses_reader(path_type(file))

    pd.testing.assert_frame_equal(
        result,
        pd.DataFrame({"Inferred structure": ["gm|0", "gm-AE|1", "gm-AE|12"], "Theo (Da)": [498.0, 500.0, 600.0]}),
    )
    assert result.attrs["file"] == "masses.csv"


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
