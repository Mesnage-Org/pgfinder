import logging

import pytest
import numpy as np
import pandas as pd
import pgfinder.masscalc as masscalc

mass_list = pd.concat(
    [
        pd.read_csv("data/masses/test_masses.csv"),
    ]
)


@pytest.fixture
def code_masses():
    return masscalc.component_masses()


@pytest.fixture(params=mass_list["Structure"])
def struct_mass(request):
    # This should return a test case for each structure with a known mass.
    return mass_list.loc[mass_list["Structure"] == request.param]


def test_mass(caplog, struct_mass: pd.DataFrame, code_masses: pd.DataFrame):
    caplog.set_level(logging.INFO)
    Structure = struct_mass["Structure"].iloc[0]
    Monoisotopicmass = struct_mass["Monoisotopicmass"].iloc[0]  # From test data file
    logging.info(
        "Mass difference: "
        + f"{(np.around(masscalc.mass(Structure, code_masses), decimals=4) - Monoisotopicmass):.14f}"
    )  # Record mass difference
    assert (
        np.around(masscalc.mass(Structure, code_masses), decimals=4) == Monoisotopicmass
    )


def test_mass_warning(caplog, code_masses: pd.DataFrame):
    with pytest.warns(UserWarning, match=r"Unmatched characters in structure"):
        masscalc.mass("gm-jvi", code_masses)


def test_component_masses():
    assert list(masscalc.component_masses().columns) == [
        "Code",
        "Structure",
        "Monoisotopicmass",
    ]
