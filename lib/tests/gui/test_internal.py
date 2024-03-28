"""Tests of the gui.internal sub-module."""

from pathlib import Path

import pandas as pd
import pytest

from pgfinder.gui import internal
from pgfinder import pgio


@pytest.mark.parametrize(
    ("upload", "lib_dir", "target"),
    [
        pytest.param(
            {"content": None, "name": "e_coli_monomers_simple.csv"},
            internal.MASS_LIB_DIR,
            pgio.theo_masses_reader(internal.MASS_LIB_DIR / "e_coli_monomers_simple.csv"),
            id="E. coli simple mass library",
        ),
        pytest.param(
            {"content": None, "name": "c_diff_monomers_complex.csv"},
            internal.MASS_LIB_DIR,
            pgio.theo_masses_reader(internal.MASS_LIB_DIR / "c_diff_monomers_complex.csv"),
            id="C. diff complex mass library",
        ),
        pytest.param(
            {"content": None, "name": "e_coli.csv"},
            internal.REF_MASS_LIB_DIR,
            pd.read_csv(internal.REF_MASS_LIB_DIR / "e_coli.csv"),
            id="E. coli reference masses library",
        ),
        pytest.param(
            {"content": None, "name": "e_coli.csv"},
            internal.TARGET_STRUCTURE_LIB_DIR,
            pd.read_csv(internal.TARGET_STRUCTURE_LIB_DIR / "e_coli.csv"),
            id="E. coli target structure library",
        ),
        pytest.param(
            {"content": None, "name": "b_subtilis.csv"},
            internal.TARGET_STRUCTURE_LIB_DIR,
            pd.read_csv(internal.TARGET_STRUCTURE_LIB_DIR / "b_subtilis.csv"),
            id="B. subtilis target structure library",
        ),
        # pytest.param(
        #     {"content": "", "name": ""},
        #     None,
        #     pgio.ms_file_reader(),
        #     id="Mass Spec file."
        # )
    ],
)
def test_upload_reader(upload: dict, lib_dir: Path, target: pd.DataFrame) -> None:
    """Test the generic upload_reader() function."""
    test_file = internal.upload_reader(upload, lib_dir)
    pd.testing.assert_frame_equal(test_file, target)


def test_ms_upload_reader() -> None:
    """
    Test the Mass specific ms_upload_reader().

    No test implemented, this is a very thin wrapper around pgio.ms_file_reader().
    """
    pass


@pytest.mark.parametrize(
    ("upload", "target"),
    [
        pytest.param(
            {"content": None, "name": "e_coli_monomers_simple.csv"},
            pgio.theo_masses_reader(internal.MASS_LIB_DIR / "e_coli_monomers_simple.csv"),
            id="E. coli simple mass library",
        ),
        pytest.param(
            {"content": None, "name": "c_diff_monomers_complex.csv"},
            pgio.theo_masses_reader(internal.MASS_LIB_DIR / "c_diff_monomers_complex.csv"),
            id="C. diff complex mass library",
        ),
        pytest.param(
            {
                "content": str.encode(
                    "Structure,Monoisotopicmass\ngm|0,498.206090\ngm-gm|0,976.385965\n\ngm-gm-gm|0,1454.565840"
                ),
                "name": "user_masses.csv",
            },
            pgio.theo_masses_reader(internal.MASS_LIB_DIR / "e_coli_monomers_complex.csv").head(3),
            id="User provided file.",
        ),
    ],
)
def test_theo_masses_upload_reader(upload: dict, target: pd.DataFrame) -> None:
    """Test the Theoretical Masses specific theo_masses_upload_reader()."""
    test_file = internal.theo_masses_upload_reader(upload)
    print(f"{test_file=}")
    print(f"{target=}")
    pd.testing.assert_frame_equal(test_file, target)


def test_uploaded_file() -> None:
    """Test the uploaded_file() function."""
