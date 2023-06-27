from pyio import msData, massLibrary, enabledModifications, ppmTolerance, cleanupWindow

theo_masses = pgio.theo_masses_upload_reader(massLibrary.to_py())


def analyze(virt_file):
    ms_data = pgio.ms_upload_reader(virt_file)
    matched = matching.data_analysis(
        ms_data, theo_masses, cleanupWindow, enabledModifications, ppmTolerance
    )
    return pgio.dataframe_to_csv_metadata(matched, wide=True)


{f["name"]: analyze(f) for f in msData.to_py()}
