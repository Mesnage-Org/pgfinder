"""Package initialisation"""

from importlib.metadata import version
from pkgutil import get_data

import yaml

from pgfinder.utils import dict_to_decimal

PARAMETERS_FILE = "config/parameters.yaml"
PARAMETERS = get_data(__package__, PARAMETERS_FILE)
PARAMETERS = yaml.safe_load(PARAMETERS)
PARAMETERS = dict_to_decimal(PARAMETERS)
COLUMNS_FILE = "config/columns.yaml"
COLUMNS = get_data(__package__, COLUMNS_FILE)
COLUMNS = yaml.safe_load(COLUMNS)
MULTIMERS = PARAMETERS["multimer"]
MOD_TYPE = PARAMETERS["mod_type"]
MASS_TO_CLEAN = PARAMETERS["mass_to_clean"]

release = version("pgfinder")
__version__ = ".".join(release.split("."[:2]))
