"""Package initialisation"""
from importlib.metadata import version
import yaml
from pkgutil import get_data
from pgfinder.utils import dict_to_decimal

PARAMETERS_FILE = "config/parameters.yaml"
PARAMETERS = get_data(__package__, PARAMETERS_FILE)
PARAMETERS = yaml.safe_load(PARAMETERS)
PARAMETERS = dict_to_decimal(PARAMETERS)
MULTIMERS = PARAMETERS["multimer"]
MOD_TYPE = PARAMETERS["mod_type"]
MASS_TO_CLEAN = PARAMETERS["mass_to_clean"]

release = version("pgfinder")
__version__ = ".".join(release.split("."[:2]))
