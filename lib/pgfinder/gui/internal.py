"""Functions used in uploading files from the WebUI."""

import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

from pgfinder import pgio

# Consider switching to using the import importlib.resources as pkg_resources method of loading files that are included
# as part of the package rather than a plain open()
MASS_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "masses"
REF_MASS_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "reference_masses"
TARGET_STRUCTURE_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "target_structures"


def upload_reader(upload: dict, lib_dir: Path) -> pd.DataFrame:
    """
    Load a built-in library if no content was uploaded.

    Handles loading theoretical masses, mass spectroscopy files, reference masses and target structures.

    Parameters
    ----------
    upload: dict
        Dictionary that contains a key 'name' with the value of the file to be uploaded.
    lib_dir: Path
        Path to the directory containing the file to be loaded.

    Returns
    -------
    pd.DataFrame
        Returns a Pandas DataFrame of the CSV file.
    """
    if upload["content"] is None:
        upload["content"] = open(lib_dir / upload["name"], "rb").read()

    with uploaded_file(upload) as file:
        # How we load the file depends on the type of library
        if lib_dir.parts[-1] == "masses":
            return pgio.theo_masses_reader(file)
        elif lib_dir is None:
            return pgio.ms_file_reader(file)
        return pd.read_csv(file)


def ms_upload_reader(upload: dict) -> pd.DataFrame:
    with uploaded_file(upload) as file:
        return pgio.ms_file_reader(file)


def theo_masses_upload_reader(upload: dict) -> pd.DataFrame:
    """Attempt to load a built-in library if no content was uploaded."""

    if upload["content"] is None:
        upload["content"] = open(MASS_LIB_DIR / upload["name"], "rb").read()

    with uploaded_file(upload) as file:
        return pgio.theo_masses_reader(file)


@contextmanager
def uploaded_file(upload: dict):
    with tempfile.TemporaryDirectory() as tempdir:
        file = Path(tempdir) / upload["name"]
        with open(file, "wb") as f:
            f.write(upload["content"])
        yield file
