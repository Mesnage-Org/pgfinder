"""Utilities"""
from argparse import Namespace
import logging
from pathlib import Path
from typing import Union, List, Dict

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
    return Path().cwd() if path == './' else Path(path)



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
