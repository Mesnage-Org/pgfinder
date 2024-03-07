"""Test the matching process"""

from pathlib import Path

import pandas as pd
import pytest

import pgfinder.matching as matching
from pgfinder.errors import UserError
from pgfinder.matching import calculate_ppm_delta, consolidate_results, pick_most_likely_structures

BASE_DIR = Path.cwd()
RESOURCES = BASE_DIR / "tests" / "resources"


def test_filtered_theo(raw_data, theo_masses, ppm):
    # this crude test just shows that the code runs
    # a better test would check that the data frame returned is correct
    matching.filtered_theo(raw_data, theo_masses, ppm)


def test_filtered_theo_no_match(raw_data_no_match, theo_masses, ppm):
    with pytest.raises(
        UserError,
        match="No matches were found for this search. Please check your database or increase mass tolerance.",
    ):
        matching.filtered_theo(raw_data_no_match, theo_masses, ppm)


def test_calculate_ppm_delta(sample_df: pd.DataFrame, df_diff_ppm: pd.DataFrame) -> None:
    """Test addition of PPM column."""
    pd.testing.assert_frame_equal(calculate_ppm_delta(sample_df, observed="obs", theoretical="exp"), df_diff_ppm)


def test_pick_most_likely_structures() -> None:
    """Test picking the most likely structure based on ppm"""
    long_df = pd.read_csv(RESOURCES / "long_results.csv")
    wide_df = pd.read_csv(RESOURCES / "wide_results.csv")

    reshaped_long_df = pick_most_likely_structures(long_df, 1)

    pd.testing.assert_frame_equal(reshaped_long_df, wide_df, check_dtype=False)


def test_consolidation(unconsolidated_df: pd.DataFrame, unconsolidated_and_consolidated_df: pd.DataFrame) -> None:
    """Test the post-processing structure / intensity consolidation step"""
    pd.testing.assert_frame_equal(consolidate_results(unconsolidated_df), unconsolidated_and_consolidated_df)
