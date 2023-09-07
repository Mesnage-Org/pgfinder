import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

from pgfinder import pgio

MASS_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "masses"


def theo_masses_upload_reader(upload: dict) -> pd.DataFrame:
    # Attempt to load a built-in library if no content was uploaded
    if upload["content"] is None:
        upload["content"] = open(MASS_LIB_DIR / upload["name"], "rb").read()

    with uploaded_file(upload) as file:
        return pgio.theo_masses_reader(file)


def ms_upload_reader(upload: dict) -> pd.DataFrame:
    with uploaded_file(upload) as file:
        return pgio.ms_file_reader(file)


@contextmanager
def uploaded_file(upload: dict):
    with tempfile.TemporaryDirectory() as tempdir:
        file = Path(tempdir) / upload["name"]
        with open(file, "wb") as f:
            f.write(upload["content"])
        yield file
