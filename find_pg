#!/usr/bin/env python3
"""Run pgfinder at the command line."""
import argparse as arg
import logging
from pathlib import Path
from typing import Union
import warnings

from pgfinder.matching import data_analysis
from pgfinder.pgio import (
    ms_file_reader,
    theo_masses_reader,
    dataframe_to_csv,
    dataframe_to_csv_metadata,
)
from pgfinder.logs.logs import LOGGER_NAME
from pgfinder.utils import update_config
from pgfinder.pgio import read_yaml

LOGGER = logging.getLogger(LOGGER_NAME)


def create_parser() -> arg.ArgumentParser:
    """Create a parser for reading options."""
    parser = arg.ArgumentParser(
        description="Process sample. Additional arguments over-ride those in the configuration file."
    )
    parser.add_argument(
        "-c", "--config_file", dest="config_file", required=True, help="Path to a YAML configuration file."
    )
    parser.add_argument("--input_file", dest="input_file", required=False, help="Input File")
    parser.add_argument("--ppm_tolerance", dest="ppm_tolerance", type=float, required=False, help="PPM Toleraance.")
    parser.add_argument("--masses_file", dest="masses_file", type=str, required=False, help="Theoretical masses file.")
    parser.add_argument("--time_delta", dest="time_delta", type=int, required=False, help="Time delta.")
    parser.add_argument("--mod_list", dest="mod_list", type=list, required=False, help="Module List.")
    parser.add_argument("--output_dir", dest="output_dir", type=str, required=False, help="Output directory.")
    parser.add_argument("--warnings", dest="warnings", type=str, required=False, help="Whether to ignore warnings.")
    parser.add_argument("--quiet", dest="quiet", type=bool, required=False, help="Supress output.")

    return parser


def process_file(
    input_file: Union[str, Path],
    masses_file: Union[str, Path],
    mod_list: list,
    ppm_tolerance: float = 0.5,
    time_delta: int = 10,
    output_dir: Union[str, Path] = Path("./"),
):
    """Process files"""
    df = ms_file_reader(input_file)

    masses = theo_masses_reader(masses_file)
    LOGGER.info(f"PPM Tolerance                      : {ppm_tolerance}")
    LOGGER.info(f"Time Delta                         : {time_delta}")

    results = data_analysis(
        raw_data_df=df,
        theo_masses_df=masses,
        rt_window=time_delta,
        enabled_mod_list=mod_list,
        user_ppm=ppm_tolerance,
    )
    LOGGER.info("Processing complete!")
    dataframe_to_csv_metadata(save_filepath=output_dir, output_dataframe=results)
    LOGGER.info(f"Metadata save to                   : {output_dir}")
    dataframe_to_csv(save_filepath=output_dir, filename="results.csv", output_dataframe=results)
    LOGGER.info(f"Results saved to                   : {output_dir / 'results.csv'}")


def main():
    """Run processing."""

    # Parse command line options, load config and update with command line options
    parser = create_parser()
    args = parser.parse_args()
    config = read_yaml(args.config_file)
    config = update_config(config, args)

    LOGGER.info(f"Configuration file loaded from     : {args.config_file}")
    LOGGER.info(f'Input file                         : {config["input_file"]}')

    # Optionally ignore all warnings or just show deprecation warnings
    if config["warnings"] == "ignore":
        warnings.filterwarnings("ignore")
        LOGGER.info("NB : All warnings have been turned off for this run.")
    elif config["warnings"] == "deprecated":

        def fxn():
            warnings.warn("deprecated", DeprecationWarning)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fxn()
    if config["quiet"]:
        LOGGER.setLevel("ERROR")

    process_file(
        input_file=config["input_file"],
        masses_file=config["masses_file"],
        ppm_tolerance=config["ppm_tolerance"],
        time_delta=config["time_delta"],
        mod_list=config["mod_list"],
        output_dir=config["output_dir"],
    )


if __name__ == "__main__":
    main()
