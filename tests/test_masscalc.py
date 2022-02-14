import pytest
import pandas as pd
import pgfinder.masscalc as masscalc

mass_list = pd.concat(
    [
        pd.read_csv("data/masses/c_diff_monomer_masses.csv"),
        pd.read_csv("data/masses/e_coli_monomer_masses.csv"),
        pd.read_csv("data/masses/test_monomer_masses.csv"),
    ]
)


@pytest.fixture(params=mass_list["Structure"])
def struct_mass(request):
    return mass_list.loc[mass_list["Structure"] == request.param]


def test_mass(struct_mass: pd.DataFrame):
    Structure = struct_mass["Structure"].iloc[0]
    Monoisotopicmass = struct_mass["Monoisotopicmass"].iloc[0]
    assert masscalc.mass(Structure) == Monoisotopicmass
