"""Utilities"""

import logging
from argparse import Namespace
from decimal import Decimal
from pathlib import Path
from typing import Dict, Union

from pgfinder.logs.logs import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)

# FIXME : Set precision, ultimately this _shouldn't_ be handled here but instead moved to find_pg.py and
#         defined in the config.yaml that is read in, dirty hard-coded hack for now to get things working so I can
#         implement the delta_ppm feature.
#
#         HOWEVER : You can't currently set this globally because in clean_up() the .quantize() method is used to round
#         things up to "0.00001" which is currently hard coded. Thus the place to do the tidying is likely under
#         clean_up() but it should be flexible and a user specified option rather than hard coded.
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
            except:  # noqa: E722
                pass
    return dictionary
