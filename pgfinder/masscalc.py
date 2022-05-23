import logging
import importlib.resources as resources
import re
import warnings

import pandas as pd

import pgfinder

from pgfinder.logs.logs import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)


def component_masses() -> pd.DataFrame:
    """Returns a data frame with columns 'Code', 'Structure', 'Monoisotopicmass'.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of component masses.
    """
    file = resources.open_text(pgfinder, "component_masses.csv")
    return pd.read_csv(
        file,
        dtype={"Code": "string", "Structure": "string", "Monoisotopicmass": "float64"},
    )


def component_regex(component_masses: pd.DataFrame) -> str:
    """Returns a regular expression string capturing 'Codes' to be associated with masses.

    Returns
    -------
    str
        String of the code associated with each mass.
    """
    component_masses = component_masses.sort_values(
        by="Code", ascending=False, key=lambda x: x.str.len()
    )  # Sort by code length high to low
    Code = component_masses["Code"].apply(re.escape)
    return Code.str.cat(sep="|")


def mass(structure: str, component_masses: pd.DataFrame) -> float:
    """Returns a 'Monoisotopicmass' given a 'Structure' and the masses of its components.

    Parameters
    ----------
    structure: str
        The structure to search for.
    component_masses: pd.DataFrame
        Pandas DataFrame from which the mass is extracted.

    Returns
    -------
    float
        The mass associated with a given structure.
    """
    structure = "H2O" + structure  # Always add water
    regex = component_regex(component_masses)
    residual = re.sub(regex, "", structure)
    if len(residual) > 0:
        warnings.warn("Unmatched characters in structure: " + residual)
    components = re.findall(regex, structure)
    components_df = pd.DataFrame(components, columns=["Code"], dtype="string")
    component_masses_filtered = pd.merge(
        how="left",
        left=components_df,
        right=component_masses,
        left_on="Code",
        right_on="Code",
    )

    LOGGER.info(
        component_masses_filtered.to_string(max_rows=component_masses_filtered.shape[0] + 1)
    )  # Log dataframe used in mass calc

    # Count MurNAc
    # Take away two hydrogen per "internal" MurNAc (2 x 1.0078Da)
    n_murnac = (
        int(component_masses_filtered.Structure[component_masses_filtered.Structure.str.contains("MurN")].count()) - 1
    )  # One MurNAc is terminal

    murnac_mass_adjust = n_murnac * 2 * 1.0078

    LOGGER.info("Internal MurNAc: " + str(n_murnac))
    LOGGER.info("Mass adjustment for internal MurNAcs: -" + str(murnac_mass_adjust))

    return component_masses_filtered.Monoisotopicmass.sum() - murnac_mass_adjust
