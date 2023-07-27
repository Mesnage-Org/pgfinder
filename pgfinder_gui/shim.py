import io
import json
import sys
import tempfile
from pathlib import Path, PurePath
from typing import Dict

import pandas as pd

from pgfinder import matching, pgio

MASS_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "masses"


def mass_library_index() -> Dict:
    return json.load(open(MASS_LIB_DIR / "index.json"))


def run_analysis():
    from pyio import (
        cleanupWindow,
        enabledModifications,
        massLibrary,
        msData,
        ppmTolerance,
    )

    theo_masses = theo_masses_upload_reader(massLibrary.to_py())

    def analyze(virt_file):
        ms_data = ms_upload_reader(virt_file)
        matched = matching.data_analysis(ms_data, theo_masses, cleanupWindow, enabledModifications, ppmTolerance)
        return pgio.dataframe_to_csv_metadata(matched, wide=True)

    return {f["name"]: analyze(f) for f in msData.to_py()}


def theo_masses_upload_reader(upload: dict) -> pd.DataFrame:
    """For reading theoretical masses from an interactive jupyter notebook with a file upload widget.

    Parameters
    ----------
    upload: dict
        Dictionary of properties of a file uploaded using
        `ipywidgets <https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#File-Upload>`_

    Returns
    -------
    pd.DataFrame
        Pandas Dataframe of theoretical masses.
    """

    filename = upload["name"]
    file_contents = open(MASS_LIB_DIR / filename, "rb").read() if upload["content"] is None else upload["content"]

    theo_masses_df = pd.read_csv(io.BytesIO(file_contents))
    theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    theo_masses_df.attrs["file"] = PurePath(filename).name
    return theo_masses_df


def ms_upload_reader(upload: dict) -> pd.DataFrame:
    """For reading from an interactive jupyter notebook with a file upload widget.

    Parameters
    ----------
    upload: dict
        Dictionary of properties of a file uploaded using
       `ipywidgets <https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#File-Upload>`_

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of mass information
    """
    filename = upload["name"]
    file_contents = upload["content"]
    file_temp = tempfile.NamedTemporaryFile(delete=False)
    file_temp.write(file_contents)
    file = file_temp.name

    if not filename.find("ftrs") == -1:
        return_df = pgio.ftrs_reader(file)
    elif not filename.find("txt") == -1:
        return_df = pgio.maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["file"] = PurePath(filename).name
    return return_df
