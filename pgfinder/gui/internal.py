import io
import sys
import tempfile
from pathlib import Path, PurePath

import pandas as pd

from pgfinder import pgio

MASS_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "masses"


def theo_masses_upload_reader(upload: dict) -> pd.DataFrame:
    filename = upload["name"]
    file_contents = open(MASS_LIB_DIR / filename, "rb").read() if upload["content"] is None else upload["content"]

    theo_masses_df = pd.read_csv(io.BytesIO(file_contents))
    theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    theo_masses_df.attrs["file"] = PurePath(filename).name
    return theo_masses_df


def ms_upload_reader(upload: dict) -> pd.DataFrame:
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
