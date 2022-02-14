import importlib.resources as resources
import re

import pandas as pd

import pgfinder


def component_masses() -> pd.DataFrame:
    """Returns a data frame with columns 'Code', 'Structure', 'Monoisotopicmass'."""
    file = resources.open_text(pgfinder, "component_masses.csv")
    return pd.read_csv(file)


def component_regex(component_masses: pd.DataFrame) -> str:
    """Returns a regular expression string capturing 'Codes' to be associated with masses."""
    component_masses = component_masses.sort_values(
        by="Code", ascending=False, key=lambda x: x.str.len()
    )  # Sort by code length high to low
    Code = component_masses["Code"].apply(re.escape)
    return Code.str.cat(sep="|")


def mass(code: str) -> float:
    """Returns a 'Monoisotopicmass' given a 'Code'."""
    return 0.000
