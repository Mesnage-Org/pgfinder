"""Package initialisation"""
import logging
from pgfinder.pgio import read_yaml
from pgfinder.logs.logs import setup_logger, LOGGER_NAME

LOGGER = setup_logger()
LOGGER = logging.getLogger(LOGGER_NAME)

PARAMETERS_FILE = "config/parameters.yaml"
PARAMETERS = read_yaml(PARAMETERS_FILE)
LOGGER.info(f"Loaded parameters from file : {PARAMETERS_FILE}")
MULTIMERS = PARAMETERS["multimer"]
MOD_TYPE = PARAMETERS["mod_type"]
MASS_TO_CLEAN = PARAMETERS["mass_to_clean"]
