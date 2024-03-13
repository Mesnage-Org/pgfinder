#!/usr/bin/env python3
"""Run pgfinder at the command line."""
import argparse as arg
import ast
import importlib.resources as pkg_resources
import logging
import warnings
from pathlib import Path

import yaml

from pgfinder.errors import UserError
from pgfinder.logs.logs import LOGGER_NAME, setup_logger
from pgfinder.matching import data_analysis
from pgfinder.pgio import (
    dataframe_to_csv_metadata,
    default_filename,
    ms_file_reader,
    read_yaml,
    theo_masses_reader,
)
from pgfinder.utils import update_config

LOGGER = setup_logger()
LOGGER = logging.getLogger(LOGGER_NAME)


def create_parser() -> arg.ArgumentParser:
    """Create a parser for reading options."""
    parser = arg.ArgumentParser(
        description="Process sample. Additional arguments over-ride those in the configuration file."
    )
    parser.add_argument(
        "-c", "--config_file", dest="config_file", required=False, help="Path to a YAML configuration file."
    )
    parser.add_argument("--input_file", dest="input_file", required=False, help="Input File")
    parser.add_argument("--ppm_tolerance", dest="ppm_tolerance", type=float, required=False, help="PPM Toleraance.")
    parser.add_argument(
        "--consolidation_ppm",
        dest="consolidation_ppm",
        type=float,
        required=False,
        help="Maximum absolute ppm distance between consolidated structures.",
    )
    parser.add_argument("--masses_file", dest="masses_file", type=str, required=False, help="Theoretical masses file.")
    parser.add_argument("--time_delta", dest="time_delta", type=int, required=False, help="Time delta.")
    parser.add_argument(
        "--mod_list", dest="mod_list", type=ast.literal_eval, required=False, help="Modifications to include."
    )
    parser.add_argument("--output_dir", dest="output_dir", type=str, required=False, help="Output directory.")
    parser.add_argument("--warnings", dest="warnings", type=str, required=False, help="Whether to ignore warnings.")
    parser.add_argument("--quiet", dest="quiet", type=bool, required=False, help="Supress output.")
    parser.add_argument(
        "--float_format", dest="float_format", type=int, required=False, help="Decimal places in output."
    )

    return parser


def process_file(
    input_file: str | Path,
    masses_file: str | Path,
    mod_list: list,
    ppm_tolerance: float = 10,
    consolidation_ppm: float = 1,
    time_delta: int = 0.5,
    output_dir: str | Path = "./",
    float_format: int = 4,
    to_csv: dict = None,
):
    """Process files

    Parameters
    ----------
    input_file : str | Path
        Mass Spectrometry input file to process.
    masses_file : str | Path
        Input file of known masses.
    mod_list : list
        Modifications to include.
    ppm_tolerance : float
        Parts Per Million tolerance for matching.
    time_delta : int
        Time difference.
    output_dir : str | Path
        Output directory where results are written to.
    float_format : int
       Decimal places to use in CSV files.
    to_csv: dict
       Dictionary of options to pass to pd.to_csv(), primarly used to overwrite existing files.
    """
    input_file = Path(input_file)
    masses_file = Path(masses_file)
    output_dir = Path(output_dir)

    df = ms_file_reader(input_file)

    masses = theo_masses_reader(masses_file)
    LOGGER.info(f"PPM Tolerance                      : {ppm_tolerance}")
    LOGGER.info(f"Time Delta                         : {time_delta}")

    results = data_analysis(
        raw_data_df=df,
        theo_masses_df=masses,
        rt_window=time_delta,
        enabled_mod_list=mod_list,
        ppm_tolerance=ppm_tolerance,
        consolidation_ppm=consolidation_ppm,
    )
    LOGGER.info("Processing complete!")
    filename = default_filename()
    dataframe_to_csv_metadata(
        save_filepath=output_dir,
        output_dataframe=results,
        filename=filename,
        float_format=f"%.{float_format}f",
    )
    LOGGER.info(f"Results with metadata saved to      : {output_dir}/{filename}")


def main():
    """Run processing."""

    try:
        # Parse command line options, load config and update with command line options
        parser = create_parser()
        args = parser.parse_args()
        if args.config_file is not None:
            config = read_yaml(args.config_file)
            LOGGER.info(f"Configuration file loaded from     : {args.config_file}")
        else:
            default_config = pkg_resources.open_text(__package__, "default_config.yaml")
            config = yaml.safe_load(default_config.read())
            LOGGER.info("Default configuration file loaded.")
        config = update_config(config, args)

        # Optionally ignore all warnings or just show deprecation warnings
        if config["warnings"] == "ignore":
            warnings.filterwarnings("ignore")
            LOGGER.info("NB : All warnings have been turned off for this run.")
        elif config["warnings"] == "deprecated":

            def fxn():
                warnings.warn("deprecated", DeprecationWarning, stacklevel=2)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fxn()
        if config["quiet"]:
            LOGGER.setLevel("ERROR")

        process_file(
            input_file=config["input_file"],
            masses_file=config["masses_file"],
            ppm_tolerance=config["ppm_tolerance"],
            consolidation_ppm=config["consolidation_ppm"],
            time_delta=config["time_delta"],
            mod_list=config["mod_list"],
            output_dir=config["output_dir"],
            float_format=config["float_format"],
        )
    except UserError as e:
        # Avoid dumping a whole stack-trace if it's the user who's done something wrong
        LOGGER.error(e)


if __name__ == "__main__":
    main()
