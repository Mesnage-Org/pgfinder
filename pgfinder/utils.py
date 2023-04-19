"""Utilities"""
from argparse import Namespace
from decimal import *
import logging
from pathlib import Path
from typing import Union, Dict

import pandas as pd

from pgfinder.logs.logs import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)

# FIXME : Set precision, ultimately this _shouldn't_ be handled here but instead moved to find_pg.py and
#         defined in the config.yaml that is read in, dirty hard-coded hack for now to get things working so I can
#         implement the delta_ppm feature.
#
#         HOWEVER : You can't currently set this globally because in clean_up() the .quantize() method is used to round
#         things up to "0.00001" which is currently hard coded. Thus the place to do the tidying is likely under clean_up()
#         but it should be flexible and a user specified option rather than hard coded.
# getcontext().prec = 5


def convert_path(path: Union[str, Path]) -> Path:
    """Ensure path is Path object.

    Parameters
    ----------
    path: Union[str, Path]
        Path to be converted.

    Returns
    -------
    Path
        pathlib Path
    """
    return Path().cwd() if path == "./" else Path(path)


def update_config(config: dict, args: Union[dict, Namespace]) -> Dict:
    """Update the configuration with any arguments

    Parameters
    ----------
    config: dict
        Dictionary of configuration (typically read from YAML file specified with '-c/--config <filename>')
    args: Namespace
        Command line arguments
    Returns
    -------
    Dict
        Dictionary updated with command arguments.
    """
    args = vars(args) if isinstance(args, Namespace) else args

    config_keys = config.keys()
    for arg_key, arg_value in args.items():
        if arg_key in config_keys and arg_value is not None:
            original_value = config[arg_key]
            config[arg_key] = arg_value
            LOGGER.info(f"Updated config config[{arg_key}] : {original_value} > {arg_value} ")
    config["input_file"] = convert_path(config["input_file"])
    config["masses_file"] = convert_path(config["masses_file"])
    config["output_dir"] = convert_path(config["output_dir"])
    return config


def dict_to_decimal(dictionary: dict) -> dict:
    """Recursively convert any floats in a dictionary to Decimal.

    Parameters
    ----------
    dictionary: dict
        Dictionary to be converted.

    Returns
    -------
    dict
        Dictionary with floats converted to Decimal
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dict_to_decimal(value)
        else:
            try:
                dictionary[key] = Decimal(value)
            except:
                pass
    return dictionary


def calculate_ppm_delta(
    df: pd.DataFrame,
    observed: str = "mwMonoisotopic",
    theoretical: str = "theo_mwMonoisotopic",
    diff: str = "diff_ppm",
) -> pd.DataFrame:
    """Calculate the difference in Parts Per Million between observed and theoretical masses.

    The PPM difference between observed and theoretical mass is calculated as...

    .. math:: (1000000 * (obs - theor)) / theor

    The function ensures the column is placed after the theoretical mass column to facilitate its use.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas DataFrame of results.
    observed : str
        Variable that defines the observed PPM.
    theoretical : str
        Variable that defines the theoretical PPM.
    diff: str
        Variable to be created that holds the difference in PPM.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame with difference noted in column diff_ppm.

    """
    column_order = list(df.columns)
    theoretical_position = column_order.index(theoretical) + 1
    df.insert(theoretical_position, diff, (1000000 * (df[observed] - df[theoretical])) / df[theoretical])
    LOGGER.info("Difference in PPM calculated.")
    return df
