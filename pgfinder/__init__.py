"""Package initialisation"""
from pkg_resources import get_distribution, DistributionNotFound

from pgfinder.logs.logs import setup_logger

LOGGER = setup_logger()
