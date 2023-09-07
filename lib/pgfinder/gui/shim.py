from pgfinder import matching, pgio, validation
from pgfinder.gui.internal import (
    MASS_LIB_DIR,
    ms_upload_reader,
    theo_masses_upload_reader,
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
