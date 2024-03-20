"""Module for gluing the WebUI together."""

from pgfinder import matching, pgio, validation
from pgfinder.gui.internal import (
    MASS_LIB_DIR,
    ms_upload_reader,
    theo_masses_upload_reader,
    builder_upload_reader,
)


def mass_library_index():
    return open(MASS_LIB_DIR / "index.json").read()


def allowed_modifications():
    return validation.allowed_modifications()


def run_analysis():
    from pyio import (
        cleanupWindow,
        consolidationPpm,
        enabledModifications,
        massLibrary,
        msData,
        ppmTolerance,
    )

    theo_masses = theo_masses_upload_reader(massLibrary.to_py())

    def analyze(virt_file):
        ms_data = ms_upload_reader(virt_file)
        matched = matching.data_analysis(
            ms_data, theo_masses, cleanupWindow, enabledModifications, ppmTolerance, consolidationPpm
        )
        return pgio.dataframe_to_csv_metadata(matched)

    return {f["name"]: analyze(f) for f in msData.to_py()}


def load_libraries() -> dict:
    """
    Load the fragments and muropeptide libraries.

    Returns
    -------
    dict :
        Fragments and muropeptides as Pandas DataFrames.
    """
    from pyio import fragmentsLibrary, muropeptidesLibrary

    return {
        "fragments": builder_upload_reader(fragmentsLibrary.to_py()),
        "muropeptides": builder_upload_reader(muropeptidesLibrary.to_py()),
    }
