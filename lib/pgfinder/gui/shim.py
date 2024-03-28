"""Module for gluing the WebUI together."""
from pathlib import Path

from pgfinder import matching, pgio, validation
from pgfinder.gui.internal import (
    MASS_LIB_DIR,
    REF_MASS_LIB_DIR,
    TARGET_STRUCTURE_LIB_DIR,
    ms_upload_reader,
    theo_masses_upload_reader,
    upload_reader,
)


def library_index(lib_dir: Path, index: str = "index.json"):
    """Load the index for a library"""
    return open(lib_dir / index).read()


def mass_library_index():
    return open(MASS_LIB_DIR / "index.json").read()


def reference_mass_library_index():
    return open(REF_MASS_LIB_DIR / "index.json").read()


def target_structure_library_index():
    return open(TARGET_STRUCTURE_LIB_DIR / "index.json").read()


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

    theo_masses = theo_masses_upload_reader(upload=massLibrary.to_py())
    # theo_masses = upload_reader(upload=massLibrary.to_py(), lib_dir=MASS_LIB_DIR)

    def analyze(virt_file):
        ms_data = ms_upload_reader(virt_file)
        # ms_data = ms_upload_reader(upload=virt_file, lib_dir=None)
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
        "fragments": upload_reader(upload=fragmentsLibrary.to_py(), lib_dir=REF_MASS_LIB_DIR),
        "muropeptides": upload_reader(upload=muropeptidesLibrary.to_py(), lib_dir=TARGET_STRUCTURE_LIB_DIR),
    }
