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

from pgfinder.errors import UserError
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
    # If we get a path, we need to convert to a string for `in` to work
    filename = PurePath(file)

    if filename.suffix == ".ftrs":
        return_df = ftrs_reader(file)
    elif filename.suffix == ".txt":
        return_df = maxquant_file_reader(file)
    else:
        raise UserError(
            (
                "The supplied data file was neither a .ftrs nor a .txt file. Please ensure that "
                "you've selected a valid Byos (.ftrs) or MaxQuant (.txt) file."
            )
        )

    return_df.attrs["file"] = filename.name
    LOGGER.info(f"Mass spectroscopy file loaded from : {filename.name}")
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
            raise UserError(
                "The supplied FTRS file could not be read. Did it come from an unsupported version of Byos?"
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


def theo_masses_reader(file: Union[str, Path]) -> pd.DataFrame:
    """Reads theoretical masses files (csv) returning a Panda Dataframe

    Parameters
    ----------
    file: Union[str, Path]

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of theoretical masses.
    """
    try:
        theo_masses_df = pd.read_csv(file)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise UserError(
            (
                "The supplied mass database doesn't contain valid CSV. Double-check that you've "
                "selected the correct file and that it's plain CSV."
            )
        ) from e
    except pd.errors.EmptyDataError as e:
        raise UserError(
            (
                "The supplied mass database was empty. Double-check that you've "
                "selected the correct file and that it contains CSV data."
            )
        ) from e

    try:
        theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    except ValueError as e:
        raise UserError(
            (
                "The supplied mass database didn't have the correct number of "
                "columns. Have you checked the format of your database against one of the built-in databases?"
            )
        ) from e
    # Check that all structures are followed by "|n" where n is one or more digits
    if not theo_masses_df["Inferred structure"].str.contains(r"\|\d+$").all():
        raise UserError(
            (
                "The supplied mass database contains structures missing the '|n' suffix encoding oligomerisation "
                "state. This should be '|1' for monomers, '|2' for dimers, '|3' for trimers, and so on."
            )
        )
    theo_masses_df.attrs["file"] = PurePath(file).name
    LOGGER.info(f"Theoretical masses loaded from     : {file}")
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
    try:
        maxquant_df = pd.read_table(file, low_memory=False)
    except pd.errors.EmptyDataError as e:
        raise UserError(
            (
                "No data was found in the supplied .txt file. Have you checked "
                "you're using the allPeptides.txt file from MaxQuant?"
            )
        ) from e
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
    try:
        maxquant_df = maxquant_df[cols_order]
    except KeyError as e:
        raise UserError(
            (
                "The supplied MaxQuant file could not be read. Have you checked "
                "you're using the allPeptides.txt file from a supported version of MaxQuant?"
            )
        ) from e

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
        f"consolidation_ppm : {output_dataframe.attrs['consolidation_ppm']}",
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
