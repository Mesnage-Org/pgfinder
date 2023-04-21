"""Test the matching process"""
import pytest

import pandas as pd

import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation
from pgfinder.matching import calculate_ppm_delta


def test_filtered_theo(raw_data, theo_masses, ppm):
    # this crude test just shows that the code runs
    # a better test would check that the data frame returned is correct
    matching.filtered_theo(raw_data, theo_masses, ppm)


def test_filtered_theo_no_match(raw_data_no_match, theo_masses, ppm):
    with pytest.raises(
        ValueError,
        match="NO MATCHES WERE FOUND for this search. Please check your database or increase mass tolerance.",
    ):
        matching.filtered_theo(raw_data_no_match, theo_masses, ppm)


def test_calculate_ppm_delta() -> None:
    """Test addition of PPM column."""
    SAMPLE_DF = pd.DataFrame({"obs": [5645.35435454, 1, 879546.3924093], "exp": [3954.49849514, 2, 879546.8974916]})
    DELTA_DF = pd.DataFrame({"diff_ppm": [427577.82345296827, -500000.0, -0.5742528357381609]})
    TARGET_DF = pd.concat([SAMPLE_DF, DELTA_DF], axis=1)

    pd.testing.assert_frame_equal(calculate_ppm_delta(SAMPLE_DF, observed="obs", theoretical="exp"), TARGET_DF)
