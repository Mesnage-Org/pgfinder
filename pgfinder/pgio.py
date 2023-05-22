"""PG Finder I/O operations"""
from importlib.metadata import version
import logging
import tempfile
from typing import Union, Dict
from pathlib import Path, PurePath
from datetime import datetime
import io
import pandas as pd
import sqlite3
import numpy as np

import yaml
from yaml.error import YAMLError

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from pgfinder.logs.logs import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)


def ms_file_reader(file) -> pd.DataFrame:
    """Read mass spec data.

    Parameters
    ----------
    file: Union[str, Path]
        Path to be loaded.

    Returns
    -------
    pd.DataFrame
        File loaded as Pandas Dataframe.
    """
    filename = file
    if not str(file).find("ftrs") == -1:
        return_df = ftrs_reader(file)
    elif not str(file).find("txt") == -1:
        return_df = maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["file"] = PurePath(filename).name
    LOGGER.info(f"Mass spectroscopy file loaded from : {file}")
    return return_df


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
        return_df = ftrs_reader(file)
    elif not filename.find("txt") == -1:
        return_df = maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["file"] = PurePath(filename).name
    LOGGER.info(f"Mass spectroscopy file loaded from  : {filename}")
    return return_df


def ftrs_reader(file: Union[str, Path]) -> pd.DataFrame:
    """Reads Features file from Byos

    Parameters
    ----------
    file: Union[str, Path]
        Feature file to be read.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of features.
    """
    with sqlite3.connect(file) as db:
        sql = "SELECT * FROM Features"
        # Reads sql database into dataframe
        ff = pd.read_sql(sql, db)
        # Adds empty "Inferred structure" and "Theo (Da)" columns
        ff["Inferred structure"] = np.nan
        ff["Theo (Da)"] = np.nan
        # Renames columns to expected column heading required for data_analysis function
        ff.rename(
            columns={
                "Id": "ID",
                "ionCount": "Ion count",
                "chargeOrder": "Charge state",
                "xicStart": "XIC start (min)",
                "xicEnd": "XIC end (min)",
                "apexRetentionTimeMinutes": "RT (min)",
                "apexMwMonoisotopic": "Obs (Da)",
                "maxIntensity": "Intensity",
                "maxAveragineCorrelation": "corrMax",
            },
            inplace=True,
        )
        # Reorder columns in dataframe to desired order, dropping unwanted columns
        cols_order = [
            "ID",
            "Ion count",
            "Charge state",
            "XIC start (min)",
            "XIC end (min)",
            "RT (min)",
            "Obs (Da)",
            "Theo (Da)",
            "Inferred structure",
            "Intensity",
        ]
        ff = ff[cols_order]

        return ff


def theo_masses_reader(input_file: Union[str, Path]) -> pd.DataFrame:
    """Reads theoretical masses files (csv) returning a Panda Dataframe

    Parameters
    ----------
    input_file: Union[str, Path]

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of theoretical masses.
    """
    theo_masses_df = pd.read_csv(input_file)
    theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    theo_masses_df.attrs["file"] = PurePath(input_file).name
    LOGGER.info(f"Theoretical masses loaded from     : {input_file}")
    return theo_masses_df


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
    file_contents = upload["content"]

    theo_masses_df = pd.read_csv(io.BytesIO(file_contents))
    theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    theo_masses_df.attrs["file"] = PurePath(filename).name
    LOGGER.info(f"Theoretical masses loaded from     : {filename}")
    return theo_masses_df


def maxquant_file_reader(file):
    """Reads maxquant files and outputs data as a dataframe.

    Parameters
    ----------
    filepath: Union[str, Path]
        Path to a text file.

    Returns
    -------
    pd.DataFrame
        Pandas Data frame
    """

    # reads file into dataframe
    maxquant_df = pd.read_table(file, low_memory=False)
    # adds inferredStructure column
    maxquant_df["Inferred structure"] = np.nan
    # adds theo_mwMonoisotopic column
    maxquant_df["Theo (Da)"] = np.nan
    # insert dataframe index as a column
    maxquant_df.reset_index(level=0, inplace=True)
    # Renames columns to expected column heading required for data_analysis function
    maxquant_df.rename(
        columns={
            "index": "ID",
            "Retention time": "RT (min)",
            "Retention length": "RT (length)",
            "Mass": "Obs (Da)",
            "Intensity": "Intensity",
        },
        inplace=True,
    )
    # Desired variables and order
    cols_order = [
        "ID",
        "RT (min)",
        "RT (length)",
        "Obs (Da)",
        "Theo (Da)",
        "Inferred structure",
        "Intensity",
    ]
    # Reorder columns in dataframe to desired order.
    maxquant_df = maxquant_df[cols_order]

    return maxquant_df


def dataframe_to_csv(
    save_filepath: Union[str, Path],
    filename: str,
    output_dataframe: pd.DataFrame,
    float_format: str = "%.4f",
    wide: bool = False,
    **kwargs,
) -> None:
    """
    Writes dataframe to csv file at desired file location

    Parameters
    ----------
    save_filepath: Union[str, Path]
        Directory to save tile to.
    filename: str
        Filename to save file to.
    output_dataframe: pd.DataFrame
        Pandas Dataframe to write to csv
    float_format: str
        Format for floating point numbers (default 4 decimal places)
    wide: bool
        Whether to reshape the data to wide format before writing to CSV.
    **kwargs
        Dictionary of keyword args passed to pd.to_csv()
    """
    if wide:
        output_dataframe = long_to_wide(df=output_dataframe.copy())
    # Ensure "index" isn't a column and output as csv file.
    if "index" in output_dataframe.columns:
        output_dataframe.drop(columns=["index"], inplace=True)
    output_dataframe.to_csv(Path(save_filepath) / filename, index=False, float_format=float_format)


def dataframe_to_csv_metadata(
    output_dataframe: pd.DataFrame,
    save_filepath: Union[str, Path] = None,
    filename: Union[str, Path] = None,
    float_format: str = "%.4f",
    wide: bool = False,
    **kwargs,
) -> Union[str, Path]:
    """If save_filepath is specified return the relative path of the output file, including the filename, otherwise
    return the .csv in the form of a string.

    Parameters
    ----------
    output_dataframe: pd.DataFrame
        Dataframe to output.
    save_filepath: Union[str, Path]
        Path to save to.
    filename: Union[str, Path]
        Filename to save to.
    float_format: str
        Format for floating point numbers (default 4 decimal places)
    wide: bool
        Whether to reshape the data to wide format before writing to CSV.
    **kwargs
        Dictionary of keyword args passed to pd.to_csv()

    Returns
    -------
    """
    release = version("pgfinder")
    _version = ".".join(release.split("."[:2]))

    metadata = [
        f"file : {str(output_dataframe.attrs['file'])}",
        f"masses_file : {str(output_dataframe.attrs['masses_file'])}",
        f"rt_window : {output_dataframe.attrs['rt_window']}",
        f"modifications : {output_dataframe.attrs['modifications']}",
        f"ppm : {output_dataframe.attrs['ppm']}",
        f"version : {_version}",
    ]
    if wide:
        output_dataframe = long_to_wide(df=output_dataframe.copy())
    # Add Metadata as first column
    output_dataframe = pd.concat([pd.DataFrame({"Metadata": metadata}), output_dataframe], axis=1)
    # Save the file to disk
    if save_filepath:
        filename = filename if filename is not None else default_filename()
        save_filepath = Path(save_filepath)
        save_filepath.mkdir(parents=True, exist_ok=True)
        output_dataframe.to_csv(save_filepath / filename, index=False, float_format=float_format)
        output = str(save_filepath / filename)
    # Store in memory as a string for returning to Notebook
    else:
        output = output_dataframe.to_csv(index=False, float_format=float_format)

    return output


def default_filename(prefix: str = "results_") -> str:
    """Generate a default filename based on the current date/time.

    Returns
    -------
    str
        Filename with format 'results_YYYY-MM-DD-hh-mm-ss.csv'.
    """
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = prefix + date_time + ".csv"

    return filename


def read_yaml(filename: Union[str, Path]) -> Dict:
    """Read a YAML file.

    Parameters
    ----------
    filename: Union[str, Path]
        YAML file to read.

    Returns
    -------
    Dict
        Dictionary of the file."""

    with Path(filename).open() as f:
        try:
            return yaml.load(f, Loader=Loader)
        except YAMLError as exception:
            LOGGER.error(exception)
            return {}


def long_to_wide(
    df: pd.DataFrame,
    id: str = "ID",
    structure_var: str = "Inferred structure",
    intensity_var: str = "Intensity",
) -> pd.DataFrame:
    """Convert long to wide format based on user specified id."""
    # Subset the variables that are to be kept in long format for subsequent merging, adding counters so we don't end
    # up with duplicates from merging long with wide format data based on id var.
    keep_columns = [
        id,
        "Ion count",
        "Charge state",
        "XIC start (min)",
        "XIC end (min)",
        "RT (min)",
        "Obs (Da)",
        "Theo (Da)",
        "Delta ppm",
        structure_var,
        intensity_var,
    ]
    keep_other = df[keep_columns].copy()
    # keep_other.rename({intensity_var: intensity_var + " (All)"}, axis=1, inplace=True)
    keep_other["match"] = keep_other.groupby(id).cumcount() + 1

    # Subset the variables that need reshaping, adding counters
    keep_reshape = [
        id,
        structure_var,
        intensity_var,
    ]
    to_reshape = df[df[structure_var].notna()][keep_reshape]
    to_reshape["match"] = to_reshape.groupby(id).cumcount() + 1

    # Retain only those instances where there is an intensity_var, this removes secondary (tertiary or quarternay etc.)
    # matches without the lowest detla-ppm. Need to track how many tied matches there are for tidying up.
    to_reshape = to_reshape[to_reshape[intensity_var].notna()]
    total_duplicate_matches = to_reshape["match"].max()
    to_reshape["match"] = to_reshape["match"].apply(str)

    # Reshape to wide _only_ instances where there are two or more candidate matches,
    # rename columns, drop the uneeded duplicate intensity columns
    wide_df = pd.pivot(to_reshape, index=id, values=[structure_var, intensity_var], columns="match")
    wide_df.columns = [" ".join(col).strip() for col in wide_df.columns.values]
    wide_df.reset_index(inplace=True)
    for x in range(2, total_duplicate_matches + 1):
        wide_df.drop(" ".join([intensity_var, str(x)]), axis=1, inplace=True)
    wide_df["match"] = 1
    to_concatenate = [x for x in wide_df.columns if structure_var in x]
    wide_df["Inferred structure (consolidated)"] = wide_df[to_concatenate].apply(
        lambda row: ",   ".join(row.values.astype(str)), axis=1
    )
    wide_df["Inferred structure (consolidated)"] = wide_df["Inferred structure (consolidated)"].str.replace(
        ",   nan", ""
    )
    wide_df.rename({"Intensity 1": "Intensity (consolidated)"}, axis=1, inplace=True)
    wide_df.drop(columns=to_concatenate, inplace=True)

    # Merge with long format data
    wide_df = keep_other.merge(wide_df, on=[id, "match"], how="outer")
    wide_df.drop("match", axis=1, inplace=True)
    wide_df.reset_index(drop=True, inplace=True)
    # Forward-fill Intensity where there are differences in ppm (deliberately blank in long so not reshaped)
    wide_df[intensity_var] = wide_df.groupby("ID")[intensity_var].ffill()
    # Hack to get desired column order
    wide_df = wide_df[
        [
            "ID",
            "Ion count",
            "Charge state",
            "XIC start (min)",
            "XIC end (min)",
            "RT (min)",
            "Obs (Da)",
            "Theo (Da)",
            "Delta ppm",
            structure_var,
            intensity_var,
            "Inferred structure (consolidated)",
            "Intensity (consolidated)",
        ]
    ]
    return wide_df
