import pytest
import numpy as np
import pandas as pd
import pgfinder.masscalc as masscalc

mass_list = pd.concat(
    [
        pd.read_csv("data/masses/c_diff_monomer_masses.csv"),
        pd.read_csv("data/masses/e_coli_monomer_masses.csv"),
    ]
)


@pytest.fixture
def code_masses():
    return masscalc.component_masses()


@pytest.fixture(params=mass_list["Structure"])
def struct_mass(request):
    # This should return a test case for each structure with a known mass.
    return mass_list.loc[mass_list["Structure"] == request.param]


def test_data_integrity():
    # Check all structures in the test set have the same monoisotopic mass.
    # (There should be the same numbers of duplicate "Structure" as
    # duplicate "Structure" AND "Monoisotopicmass".)
    mass_group_struct = mass_list.groupby(["Structure"])
    mass_group_struct = mass_group_struct.size().reset_index()

    mass_group_all = mass_list.groupby(["Structure", "Monoisotopicmass"])
    mass_group_all = mass_group_all.size().reset_index().drop("Monoisotopicmass", 1)

    pd.testing.assert_frame_equal(mass_group_struct, mass_group_all)


def test_mass(struct_mass: pd.DataFrame, code_masses: pd.DataFrame):
    Structure = struct_mass["Structure"].iloc[0]
    Monoisotopicmass = struct_mass["Monoisotopicmass"].iloc[0] # From test data file
    assert (
        np.around(masscalc.mass(Structure, code_masses), decimals=4) == Monoisotopicmass
    )


def test_component_masses():
    assert list(masscalc.component_masses().columns) == [
        "Code",
        "Structure",
        "Monoisotopicmass",
    ]
