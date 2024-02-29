import os

import pandas as pd

# BR: File paths are hard-coded here, so you need to edit the script to use it as is

# Path to input csv file
input_file_path = r"../../20200124_Ecoli_WT_d10_BGPB_01.csv"
# Path to desired output folder
output_file_path = r"../../output/"
# desired file name for output
output_file_name = "20200124_Ecoli_WT_d10_BGPB_01.xlsx"

# BR: I don't know if this is something valuable? It should give the same results,
# just without that "Consolidation PPM" picking of the closest matching structure

# If true, consolidation will use inferred_structure and Intensity
# If false,consolidate will use inferred_structure (consolidated) and Intensity (consolidated)
process_raw_data = False


def input_file_to_dataframe(input_file_path):
    dataframe = pd.read_csv(input_file_path)
    return dataframe


# BR: Either needs the formatting manually changed in Excel to appear as percentages,
# or multiplication by 100, or (best) the automatic setting of formatting via xlsxwriter


def calculate_abundance(dataframe, intensity_col):
    total_intensity = dataframe[intensity_col].sum()
    dataframe["Abundance"] = dataframe[intensity_col] / total_intensity
    return dataframe


def extract_oligomer_state(structure):
    return structure[-1]


def consolidate(input_df, structure_col_name, intensity_col_name):
    # Perform consolidation
    # BR: The x.index gets the indicies of the rows in each group (same structure name)
    # then uses those to get the intensity values from the original dataframe with .loc
    # the .idxmax() then gets the index of the max intensity, and uses that to index into
    # x, which is a series representing a given column — seems like sound logic, minus
    # inconsistent use of 'intensity_col_name'
    consolidated_df = (
        input_df.groupby(structure_col_name)
        .agg(
            {
                "RT (min)": lambda x: x[input_df.loc[x.index, intensity_col_name].idxmax()],
                intensity_col_name: "sum",
                # BR: Gave up on that `intensity_col_name` here? This seems to be inviting bugs
                "Theo (Da)": lambda x: x[input_df.loc[x.index, "Intensity"].idxmax()],
                "Delta ppm": lambda x: x[input_df.loc[x.index, "Intensity"].idxmax()],
            }
        )
        .reset_index()
    )

    return consolidated_df


def write_to_excel_file(input_df, result_df, output_file):
    # Write to Excel
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        # Write original DataFrame to Excel
        input_df.to_excel(writer, sheet_name="Data", index=False)

        # Write consolidated DataFrame to Excel, starting from 3 columns after the last column of the input DataFrame
        result_df.to_excel(writer, sheet_name="Data", startcol=input_df.shape[1] + 3, index=False)


def orchestrate(input_file, save_file_path, save_file_name, process_non_consolidated_columns: bool):
    if process_non_consolidated_columns:
        structure_col_name = "Inferred structure"
        intensity_col_name = "Intensity"
    else:
        structure_col_name = "Inferred structure (consolidated)"
        intensity_col_name = "Intensity (consolidated)"

    input_dataframe = input_file_to_dataframe(input_file)

    output_file = os.path.join(save_file_path, save_file_name)

    result_df = consolidate(input_dataframe, structure_col_name, intensity_col_name)

    # Calculate abundance
    result_df = calculate_abundance(result_df, intensity_col_name)

    # Add Oligomer state column
    result_df["Oligomer"] = result_df[structure_col_name].apply(extract_oligomer_state)

    write_to_excel_file(input_dataframe, result_df, output_file)


orchestrate(input_file_path, output_file_path, output_file_name, process_raw_data)
