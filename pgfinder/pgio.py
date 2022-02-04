import tempfile
from typing import Union
import pathlib
from pathlib import Path
import datetime
import io
import os
import pandas as pd
import sqlite3
import numpy as np
import yaml


def ms_file_reader(file) -> pd.DataFrame:
    """Read mass spec data."""
    filename = file

    if not file.find("ftrs") == -1:
        return_df = ftrs_reader(file)
    elif not file.find("txt") == -1:
        return_df = maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["filename"] = filename
    return return_df


def ms_upload_reader(upload: dict) -> pd.DataFrame:
    """For reading from an interactive jupyter notebook with a file upload widget"""
    filename = list(upload.keys())[0]
    file_contents = upload[list(upload.keys())[0]][
        "content"
    ]  # I hate this line of code
    file_temp = tempfile.NamedTemporaryFile(delete=False)
    file_temp.write(file_contents)
    file = file_temp.name

    if not filename.find("ftrs") == -1:
        return_df = ftrs_reader(file)
    elif not filename.find("txt") == -1:
        return_df = maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["filename"] = filename
    return return_df


def ftrs_reader(file):
    """Reads FTRS file from Byos
    :param filePath:
    :return dataframe:
    """
    with sqlite3.connect(file) as db:

        sql = "SELECT * FROM Features"
        # Reads sql database into dataframe
        ff = pd.read_sql(sql, db)
        # adds inferredStructure column
        ff["inferredStructure"] = np.nan
        # adds theo_mwMonoisotopic column
        ff["theo_mwMonoisotopic"] = np.nan
        # Renames columns to expected column heading required for data_analysis function
        ff.rename(
            columns={
                "Id": "ID",
                "apexRetentionTimeMinutes": "rt",
                "apexMwMonoisotopic": "mwMonoisotopic",
                "maxAveragineCorrelation": "corrMax",
            },
            inplace=True,
        )
        # Desired column order
        cols_order = [
            "ID",
            "xicStart",
            "xicEnd",
            "feature",
            "corrMax",
            "ionCount",
            "chargeOrder",
            "maxIsotopeCount",
            "rt",
            "mwMonoisotopic",
            "theo_mwMonoisotopic",
            "inferredStructure",
            "maxIntensity",
        ]
        # Reorder columns in dataframe to desired order.
        ff = ff[cols_order]

        return ff


def theo_masses_reader(file):

    """
    Reads theoretical masses files (csv)
    :param file:
    :return dataframe:
    """
    # reads csv files and converts to dataframe
    theo_masses_df = pd.read_csv(file)

    theo_masses_df.attrs["filename"] = file
    return theo_masses_df


def theo_masses_upload_reader(upload: dict) -> pd.DataFrame:
    """For reading from an interactive jupyter notebook with a file upload widget"""
    filename = list(upload.keys())[0]
    file_contents = upload[list(upload.keys())[0]][
        "content"
    ]  # I hate this line of code

    return_df = pd.read_csv(io.BytesIO(file_contents))

    return_df.attrs["filename"] = filename
    return return_df


def maxquant_file_reader(file):
    """
        Reads maxquant files and outputs data as a dataframe

    :param filepath (file should be a text file):
    :return dataframe:
    """

    # reads file into dataframe
    maxquant_df = pd.read_table(file, low_memory=False)
    # adds inferredStructure column
    maxquant_df["inferredStructure"] = np.nan
    # adds theo_mwMonoisotopic column
    maxquant_df["theo_mwMonoisotopic"] = np.nan
    # insert dataframe index as a column
    maxquant_df.reset_index(level=0, inplace=True)
    # Renames columns to expected column heading required for data_analysis function
    maxquant_df.rename(
        columns={
            "index": "ID",
            "Retention time": "rt",
            "Retention length": "rt_length",
            "Mass": "mwMonoisotopic",
            "Intensity": "maxIntensity",
        },
        inplace=True,
    )
    # Keeps only essential columns, all extraneous columns are left out.
    focused_maxquant_df = maxquant_df[
        [
            "ID",
            "mwMonoisotopic",
            "rt",
            "rt_length",
            "maxIntensity",
            "inferredStructure",
            "theo_mwMonoisotopic",
        ]
    ]
    # Desired column order
    cols_order = [
        "ID",
        "rt",
        "rt_length",
        "mwMonoisotopic",
        "theo_mwMonoisotopic",
        "inferredStructure",
        "maxIntensity",
    ]
    # Reorder columns in dataframe to desired order.
    focused_maxquant_df = focused_maxquant_df[cols_order]

    return focused_maxquant_df


def dataframe_to_csv(save_filepath: str, filename: str, output_dataframe: pd.DataFrame):
    """
    Writes dataframe to csv file at desired file location
    :param save_filepath:
    :param filename:
    :param output_dataframe:
    :return csv file:
    """

    # Combine save location and desired file name with correct formatting for output as csv file.
    write_location = save_filepath + "/" + filename + ".csv"
    output_dataframe.to_csv(write_location, index=False)


def dataframe_to_csv_metadata(
    output_dataframe: pd.DataFrame,
    save_filepath: Union[str, Path] = None,
    filename: Union[str, Path] = None,
) -> Union[str, Path]:
    """If save_filepath is specified return the relative path of the output file, including
    the filename, otherwise return the .csv in the form of a string."""

    metadata_string = yaml.dump(output_dataframe.attrs["metadata"])

    output_dataframe.insert(0, metadata_string.replace("\n", " "), "")

    if save_filepath:  # We're going to actually save the file to disk
        filename = pathlib.Path(filename or default_filename())
        write_location = os.path.join(save_filepath, filename)
        output_dataframe.to_csv(write_location, index=False)
        output = write_location
    else:  # We're going to leave it in memory as a string
        output = output_dataframe.to_csv(index=False)

    return output


def default_filename():
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "results_" + date_time + ".csv"

    return filename
