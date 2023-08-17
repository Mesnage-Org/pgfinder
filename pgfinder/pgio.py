"""PG Finder I/O operations"""
import logging
import sqlite3
from datetime import datetime
from importlib.metadata import version
from pathlib import Path, PurePath
from typing import Dict, Union

import numpy as np
import pandas as pd
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
        ftrs_52_columns = [
            "Id",
            "apexRetentionTime",
            "charges",
            "mwMonoIsotopicMass",
            "apexIntensity",
        ]

        ftrs_311_columns = [
            "Id",
            "apexRetentionTimeMinutes",
            "chargeOrder",
            "apexMwMonoisotopic",
            "maxIntensity",
        ]

        pgfinder_columns = [
            "ID",
            "RT (min)",
            "Charge",
            "Obs (Da)",
            "Intensity",
        ]

        is_ftrs_52 = set(ftrs_52_columns).issubset(ff.columns)
        is_ftrs_311 = set(ftrs_311_columns).issubset(ff.columns)

        if is_ftrs_52:
            ff.rename(
                columns=dict(zip(ftrs_52_columns, pgfinder_columns)),
                inplace=True,
            )
        elif is_ftrs_311:
            ff.rename(
                columns=dict(zip(ftrs_311_columns, pgfinder_columns)),
                inplace=True,
            )
        else:
            raise ValueError(
                "The supplied FTRS file could not be read! Did it come from an unsupported version of Byos?"
            )

        # Reorder columns in dataframe to desired order, dropping unwanted columns
        cols_order = [
            "ID",
            "RT (min)",
            "Charge",
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
            "Mass": "Obs (Da)",
        },
        inplace=True,
    )
    # Desired variables and order
    cols_order = [
        "ID",
        "RT (min)",
        "Charge",
        "Obs (Da)",
        "Theo (Da)",
        "Inferred structure",
        "Intensity",
    ]
    # Reorder columns in dataframe to desired order.
    maxquant_df = maxquant_df[cols_order]

    return maxquant_df


def dataframe_to_csv_metadata(
    output_dataframe: pd.DataFrame,
    save_filepath: Union[str, Path] = None,
    filename: Union[str, Path] = None,
    float_format: str = "%.4f",
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
