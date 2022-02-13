import pytest
import pandas as pd
import pgfinder.masscalc as masscalc

mass_list = pd.read_csv("data/masses/test_monomer_masses.csv")


@pytest.fixture(params=mass_list["Structure"])
def struct_mass(request):
    #return mass_list.iloc[[request.param]]
    return(mass_list.loc[mass_list["Structure"] == request.param])


def test_mass(struct_mass: pd.DataFrame):
    Structure = struct_mass["Structure"][1]
    Monoisotopicmass = struct_mass["Monoisotopicmass"][1]
    assert masscalc.mass(Structure) == Monoisotopicmass
