"""Matching functions"""
import logging
from decimal import Decimal

import numpy as np
import pandas as pd

from pgfinder import MULTIMERS, MOD_TYPE, MASS_TO_CLEAN
from pgfinder.logs.logs import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)


def calc_ppm_tolerance(mw: float, ppm_tol: int = 10) -> float:
    """Calculates ppm tolerance value

    Parameters
    ----------
    mw: float
        Molecular weight.
    ppm_tol: int
        PPM tolerance

    Returns
    -------
    float
        ?
    """
    return (mw * ppm_tol) / 1000000


def filtered_theo(ftrs_df: pd.DataFrame, theo_df: pd.DataFrame, user_ppm: int) -> pd.DataFrame:
    """Generate list of observed structures from theoretical masses dataframe to reduce search space.

    Parameters
    ----------
    ftrs_df: pd.DataFrame
        Features dataframe.
    theo_df: pd.DataFrame
        Theoretical dataframe.
    user_ppm: int

    Returns
    -------
    pd.DataFrame
        ?
    """
    # Match theoretical structures to raw data to generate a list of observed structures
    matched_df = matching(ftrs_df=ftrs_df, matching_df=theo_df, set_ppm=user_ppm)
    # Create dataframe containing only theo_mwMonoisotopic & inferredStructure columns from matched_df
    filtered_df = matched_df[["Inferred structure", "Theo (Da)"]].copy()
    # Drop all rows with NaN values in the Theo (Da) column
    filtered_df.dropna(subset=["Theo (Da)"], inplace=True)

    # Drop duplicate structures and masses
    filtered_df.drop_duplicates(inplace=True)

    if filtered_df.empty:
        raise ValueError(
            "NO MATCHES WERE FOUND for this search. Please check your database or increase mass tolerance."
        )

    return filtered_df


def multimer_builder(theo_df, multimer_type: int = 0):
    """Generate multimers (dimers & trimers) from observed monomers

    Parameters
    ----------
    theo_df:
        dataframe containing theoretical monomerics structures and their corresponding masses
    multimer_type: int

    Returns
    -------
    pd.DataFrame
        dataframe containing theoretical multimers and their corresponding masses
    """

    theo_mw = []
    theo_struct = []

    # Builder sub function - calculates multimer mass and name
    # FIXME : No need to use nested functions
    def builder(name, mass, mult_num: int):
        for _, row in theo_df.iterrows():
            if (
                len(row["Inferred structure"][: len(row["Inferred structure"]) - 2]) > 2
            ):  # Prevent dimer creation using just gm (input format is XX|n) X = letters n = number
                mw = row["Theo (Da)"]
                acceptor = row["Inferred structure"][: len(row["Inferred structure"]) - 2]
                donor = name
                donor_mw = mass
                theo_mw.append(Decimal(mw) + donor_mw + Decimal("-18.0106"))
                theo_struct.append(acceptor + "-" + donor + "|" + str(mult_num))

    # Call builder subfunction with different arguements based on multimer type selected
    # and calculate multimers based on peptide bond through side chain
    # if multimer_type is "peptide":
    if multimer_type == 0:
        multimer = MULTIMERS["peptide"]
    # elif multimer_type is "gycosidic":
    elif multimer_type == 1:
        multimer = MULTIMERS["gycosidic"]
    # elif multimer_type is "lactyl":
    elif multimer_type == 2:
        multimer = MULTIMERS["lactyl"]
    LOGGER.info(f"Building features for multimer type : {multimer_type}")
    [builder(molecule, Decimal(features["mass"]), features["mult_num"]) for molecule, features in multimer.items()]

    # converts lists to dataframe
    multimer_df = pd.DataFrame(list(zip(theo_mw, theo_struct)), columns=["Theo (Da)", "Inferred structure"])
    return multimer_df


def modification_generator(filtered_theo_df: pd.DataFrame, mod_type: str) -> pd.DataFrame:
    """Generates modified muropeptides (calculates new mass and add modification tag to structure name)

    Parameters
    ----------
    filtered_theo_df : pd.DataFrame
        Pandas DataFrame of theoretical masses that have been filtered.
    mod_type : str
        Modification type ???.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of ???
    """
    mod_mass = Decimal(MOD_TYPE[mod_type]["mass"])
    mod_name = MOD_TYPE[mod_type]["name"]

    obs_theo_muropeptides_df = filtered_theo_df.copy()
    # Calculate new mass of modified structure
    obs_theo_muropeptides_df["Theo (Da)"] = obs_theo_muropeptides_df["Theo (Da)"].map(lambda x: Decimal(x) + mod_mass)

    # Add modification tags to structure name
    if mod_type == "Decay":
        obs_theo_muropeptides_df["Inferred structure"] = obs_theo_muropeptides_df["Inferred structure"].map(
            lambda x: x[1 : len(x)]
        )
    elif mod_type == "Sodium" or mod_type == "Potassium":
        obs_theo_muropeptides_df["Inferred structure"] = obs_theo_muropeptides_df["Inferred structure"].map(
            lambda x: mod_name + " " + x
        )
    elif mod_type == "Nude":
        obs_theo_muropeptides_df["Inferred structure"] = obs_theo_muropeptides_df["Inferred structure"].map(
            lambda x: mod_name + x
        )
    else:
        obs_theo_muropeptides_df["Inferred structure"] = obs_theo_muropeptides_df["Inferred structure"].map(
            lambda x: x[: len(x) - 2] + " " + "(" + mod_type + ")" + " " + x[len(x) - 2 : len(x)]
        )
    return obs_theo_muropeptides_df


def matching(ftrs_df: pd.DataFrame, matching_df: pd.DataFrame, set_ppm: int) -> pd.DataFrame:
    """Match theoretical masses to observed masses within ppm tolerance.

    Parameters
    ----------
    ftrs_df: pd.DataFrame
        Features DataFrame
    matching_df: pd.DataFrame
        Matching DataFrame
    set_ppm: int

    Returns
    -------
    pd.DataFrame
        Dataframe of matches.
    """
    molecular_weights = matching_df[["Inferred structure", "Theo (Da)"]]
    matches_df = pd.DataFrame()

    for s, m in molecular_weights.itertuples(index=False):
        # FIXME: I'm not sure if it's better to convert everything to float or
        # to convert everthing to Decimal instead
        m = float(m)
        tolerance = calc_ppm_tolerance(m, set_ppm)
        mw_matches = ftrs_df[(ftrs_df["Obs (Da)"] >= m - tolerance) & (ftrs_df["Obs (Da)"] <= m + tolerance)].copy()

        # If we have matches add the structure and molecular weight then append
        if len(mw_matches.index) > 0:
            mw_matches["Inferred structure"] = s
            mw_matches["Theo (Da)"] = round(m, 4)
            matches_df = pd.concat([matches_df, mw_matches])

    # Merge with raw data
    unmatched = ftrs_df[~ftrs_df.index.isin(matches_df.index)]
    return pd.concat([matches_df, unmatched])


def clean_up(ftrs_df: pd.DataFrame, mass_to_clean: Decimal, time_delta: float) -> pd.DataFrame:
    """Clean up a DataFrame.

    Parameters
    ----------
    ftrs_df: pd.DataFrame
        Features dataframe?
    mass_to_clean: Decimal
        Mass to be cleaned.
    time_delta: float
        ?

    Returns
    -------
    pd.DataFrame:
        ?
    """
    # Get the type of adduct based on the mass_to_clean (which is a float)
    adducts = {"sodiated": Decimal("21.9819"), "potassated": Decimal("37.9559"), "decay": Decimal("203.0793")}
    adducts_keys = list(adducts.keys())
    adducts_values = list(adducts.values())
    adduct = adducts_keys[adducts_values.index(mass_to_clean)]
    # Selector substrings for generating parent and adduct dataframes
    parent = MASS_TO_CLEAN[adduct]["parent"]
    target = MASS_TO_CLEAN[adduct]["target"]

    # Generate parent dataframe - contains parents
    parent_muropeptide_df = ftrs_df.loc[ftrs_df["Inferred structure"].str.contains(parent, na=False)]

    # Generate adduct dataframe - contains adducts
    adducted_muropeptide_df = ftrs_df.loc[ftrs_df["Inferred structure"].str.contains(target, na=False)]

    # Generate copy of rawdata dataframe
    consolidated_decay_df = ftrs_df.copy()

    # Status updates (prints to console)
    if parent_muropeptide_df.empty:
        LOGGER.info(f"No {parent}  muropeptides found")
    if adducted_muropeptide_df.empty:
        LOGGER.info(f"No {target} found")
    elif mass_to_clean == adducts["sodiated"]:
        LOGGER.info(f"Processing {adducted_muropeptide_df.size} Sodium Adducts")
    elif mass_to_clean == adducts["potassated"]:
        LOGGER.info(f"Processing {adducted_muropeptide_df.size} potassium adducts")
    elif mass_to_clean == adducts["decay"]:
        LOGGER.info(f"Processing {adducted_muropeptide_df.size} in source decay products")

    # Consolidate adduct intensity with parent ions intensity
    for _y, row in parent_muropeptide_df.iterrows():
        # Get retention time value from row
        rt = row["RT (min)"]
        # Get theoretical monoisotopic mass value from row as list of values
        intact_mw = row["Theo (Da)"]

        # Work out rt window
        upper_lim_rt = rt + time_delta
        lower_lim_rt = rt - time_delta

        # Get all adducts within rt window
        ins_constrained_df = adducted_muropeptide_df[
            adducted_muropeptide_df["RT (min)"].between(lower_lim_rt, upper_lim_rt, inclusive="both")
        ]
        if not ins_constrained_df.empty:
            # Loop through each of the adducts in the RT window, the adducts
            # themselves all have structures containing the `target` string
            for _z, ins_row in ins_constrained_df.iterrows():
                ins_mw = ins_row["Theo (Da)"]

                # Compare parent masses to adduct masses
                mass_delta = abs(
                    Decimal(intact_mw).quantize(Decimal("0.00001")) - Decimal(ins_mw).quantize(Decimal("0.00001"))
                )

                # Is the mass delta the same mass as the target `mass_to_clean`?
                # If so, it's the same structure but that gets its charge from
                # the `target` ion instead of a proton as normal. In this case,
                # consolidate the intensities of the parent (H+) and adduct
                # (`target`+) ions so that the parent intensity has all of the
                # adduct intensities added to it
                if mass_delta == mass_to_clean:
                    insDecay_intensity = ins_row["Intensity"]
                    ID = row.ID
                    drop_ID = ins_row.ID
                    # Because long format leads to rows with duplicate IDs, the ["ID"]
                    # of a row is sometimes different from its index in the dataframe.
                    # Because this is sometimes but not always the case, we need this
                    # lookup line:
                    idx = consolidated_decay_df.loc[consolidated_decay_df["ID"] == ID].index[0]
                    # Make sure the row we are trying to consolidate hasn't already
                    # been consolidated and deleted!
                    if not consolidated_decay_df.loc[consolidated_decay_df["ID"] == drop_ID].empty:
                        # Transfer adduct intensity to the parent ion
                        consolidated_decay_df.at[idx, "Intensity"] += insDecay_intensity
                        # Because long format means both IDs and structures can be duplicated,
                        # only ID + structure pairs can be considered unique. Find where IDs
                        # or structures differ and retain only those in the dataframe. This is
                        # the same as *filtering out* rows in which *both* the ID and structure
                        # match the target from ins_row
                        diff_ID = consolidated_decay_df["ID"] != ins_row["ID"]
                        diff_Structure = consolidated_decay_df["Inferred structure"] != ins_row["Inferred structure"]
                        consolidated_decay_df = consolidated_decay_df[diff_ID | diff_Structure]

    return consolidated_decay_df


def data_analysis(
    raw_data_df: pd.DataFrame,
    theo_masses_df: pd.DataFrame,
    rt_window: float,
    enabled_mod_list: list,
    user_ppm=int,
) -> pd.DataFrame:
    """Perform analysis.

    Parameters
    ----------
    raw_data_df : pd.DataFrame
        User data as Pandas DataFrame.
    theo_masses_df : pd.DataFrame
        Theoretical masses as Pandas DataFrame.
    rt_window : float
        ?
    enabled_mod_list : list
        List of modules to enable.
    user_ppm : int
        ?

    Returns
    -------
    pd.DataFrame
    """
    sugar = Decimal("203.0793")
    sodium = Decimal("21.9819")
    potassium = Decimal("37.9559")
    # retention time window to look in for in source decay products (rt of parent ion plus or minus time_delta)
    time_delta_window = rt_window

    # FIXME : Should these be .copy() since Pandas DataFrames will be modified by reference I think and so any change to
    # theo or ff cascades back to theo_masses_df and raw_data_df automatically (unless that is the intention)?
    theo = theo_masses_df
    ff = raw_data_df

    LOGGER.info("Filtering theoretical masses by observed masses")
    obs_monomers_df = filtered_theo(ftrs_df=ff, theo_df=theo, user_ppm=user_ppm)
    # FIXME : Is this the logic that is required? It seems only one type of multimers will ever get built but is it not
    #         possible that there are multiple types listed in the enbaled_mod_list?
    # FIXME : Tests of the impacts here are poor.
    if "Multimers" in enabled_mod_list:
        LOGGER.info("Building multimers from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df)
        LOGGER.info("Filtering theoretical multimers by observed")
        obs_multimers_df = filtered_theo(ff, theo_multimers_df, user_ppm)
    elif "multimers_Glyco" in enabled_mod_list:
        LOGGER.info("Building multimers from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df, 1)
        LOGGER.info("Filtering theoretical multimers by observed")
        obs_multimers_df = filtered_theo(ff, theo_multimers_df, user_ppm)
    elif "Multimers_Lac" in enabled_mod_list:
        LOGGER.info("Building multimers_Lac from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df, 2)
        LOGGER.info("Filtering theoretical multimers by observed")
        obs_multimers_df = filtered_theo(ff, theo_multimers_df, user_ppm)
    else:
        obs_multimers_df = pd.DataFrame()

    LOGGER.info("Building custom search file")

    obs_theo_df = pd.concat([obs_monomers_df, obs_multimers_df]).reset_index(drop=True)

    LOGGER.info("Generating variants")

    if "Sodium" in enabled_mod_list:
        adducts_sodium_df = modification_generator(obs_theo_df, "Sodium")
    else:
        adducts_sodium_df = pd.DataFrame()

    if "Potassium" in enabled_mod_list:
        adducts_potassium_df = modification_generator(obs_theo_df, "Potassium")
    else:
        adducts_potassium_df = pd.DataFrame()

    if "Anh" in enabled_mod_list:
        anhydro_df = modification_generator(obs_theo_df, "Anh")
    else:
        anhydro_df = pd.DataFrame()

    if "DeAc" in enabled_mod_list:
        deacetyl_df = modification_generator(obs_theo_df, "DeAc")
    else:
        deacetyl_df = pd.DataFrame()

    if "DeAc_Anh" in enabled_mod_list:
        deac_anhy_df = modification_generator(obs_theo_df, "DeAc_Anh")
    else:
        deac_anhy_df = pd.DataFrame()
    if "O-Acetylated" in enabled_mod_list:
        oacetyl_df = modification_generator(obs_theo_df, "O-Acetylated")
    else:
        oacetyl_df = pd.DataFrame()

    if "Nude" in enabled_mod_list:
        nude_df = modification_generator(obs_theo_df, "Nude")
    else:
        nude_df = pd.DataFrame()

    if "Decay" in enabled_mod_list:
        decay_df = modification_generator(obs_theo_df, "Decay")
    else:
        decay_df = pd.DataFrame()

    if "Amidation" in enabled_mod_list:
        ami_df = modification_generator(obs_theo_df, "Amidated")
    else:
        ami_df = pd.DataFrame()

    if "Amidase" in enabled_mod_list:
        deglyco_df = modification_generator(obs_theo_df, "Amidase Product")
    else:
        deglyco_df = pd.DataFrame()

    if "Double_Anh" in enabled_mod_list:
        double_Anhydro_df = modification_generator(obs_theo_df, "Double_Anh")

    else:
        double_Anhydro_df = pd.DataFrame()

    master_list = [
        obs_theo_df,
        adducts_potassium_df,
        adducts_sodium_df,
        anhydro_df,
        deac_anhy_df,
        deacetyl_df,
        oacetyl_df,
        decay_df,
        nude_df,
        ami_df,
        deglyco_df,
        double_Anhydro_df,
    ]
    master_frame = pd.concat(master_list)
    master_frame = master_frame.astype({"Theo (Da)": float})
    LOGGER.info("Matching")
    matched_data_df = matching(ff, master_frame, user_ppm)
    LOGGER.info("Cleaning data")

    matched_data_df = calculate_ppm_delta(df=matched_data_df)
    matched_data_df = determine_most_likely_structure(matched_data_df.reset_index(drop=True))

    cleaned_df = clean_up(ftrs_df=matched_data_df, mass_to_clean=sodium, time_delta=time_delta_window)
    cleaned_df = clean_up(ftrs_df=cleaned_df, mass_to_clean=potassium, time_delta=time_delta_window)
    cleaned_data_df = clean_up(ftrs_df=cleaned_df, mass_to_clean=sugar, time_delta=time_delta_window)

    # set metadata
    cleaned_data_df.attrs["file"] = raw_data_df.attrs["file"]
    cleaned_data_df.attrs["masses_file"] = theo_masses_df.attrs["file"]
    cleaned_data_df.attrs["rt_window"] = rt_window
    cleaned_data_df.attrs["modifications"] = enabled_mod_list
    cleaned_data_df.attrs["ppm"] = user_ppm

    cleaned_data_df.reset_index(inplace=True)
    return cleaned_data_df


def calculate_ppm_delta(
    df: pd.DataFrame,
    observed: str = "Obs (Da)",
    theoretical: str = "Theo (Da)",
    diff: str = "Delta ppm",
) -> pd.DataFrame:
    """Calculate the difference in Parts Per Million between observed and theoretical masses.

    The PPM difference between observed and theoretical mass is calculated as...

    .. math:: (1000000 * (obs - theor)) / theor

    The function ensures the column is placed after the theoretical mass column to facilitate its use.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas DataFrame of results.
    observed : str
        Variable that defines the observed PPM.
    theoretical : str
        Variable that defines the theoretical PPM.
    diff: str
        Variable to be created that holds the difference in PPM.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame with difference noted in column diff.

    """
    column_order = list(df.columns)
    theoretical_position = column_order.index(theoretical) + 1
    df.insert(theoretical_position, diff, (1000000 * (df[observed] - df[theoretical])) / df[theoretical])
    LOGGER.info("Difference in PPM calculated.")
    return df


def determine_most_likely_structure(
    df: pd.DataFrame,
    observed_id: str = "ID",
    inferred_structure: str = "Inferred structure",
    diff: str = "Delta ppm",
    intensity: str = "Intensity",
) -> pd.DataFrame:
    """Determine the most likely structure.

    Parameters
    ----------
    df: pd.DataFrame
        Pandas Data frame for modification.
    observed_id: str
        Variable (column) within dataframe that defines the ID of observed molecules.
    inferred_structure: str
        Variable (column) within dataframe that defines the molecule identifier.
    diff: str
        Variable (column) within the dataframe that defines the difference in Parts Per Million (PPM). Default
    'Delta ppm'.
    intensity: str
        Variable (column) within dataframe that defines the intensity associated with matches.

    Returns
    -------
    pd.DataFrame
        Pandas Dataframe augmented with columns showing the most likely match (`lowest_ppm`) and the associated maximum
    intensity. The rows are sorted by molecule ID and ordered by the absolute difference in PPM within each molecule.
    """
    # Find the absolute smallest ppm, retaining whether values are negative
    abs_ppm = df[[observed_id, inferred_structure, diff]].copy()
    abs_ppm["abs_diff"] = abs_ppm[diff].abs()
    df["neg"] = np.where(df[diff] < 0, -1, 1)
    min_ppm = abs_ppm[[observed_id, "abs_diff"]].groupby([observed_id]).min("abs_diff").reset_index()
    min_ppm.columns = [observed_id, "min_abs_diff"]
    abs_ppm = abs_ppm.merge(min_ppm[[observed_id, "min_abs_diff"]], on=observed_id, how="left")
    abs_ppm = abs_ppm[[observed_id, "min_abs_diff"]].drop_duplicates()
    df = df.merge(abs_ppm, on=observed_id, how="outer")
    # Restore the sign of the smallest ppm and merge with original data
    df["min_ppm"] = df["min_abs_diff"] * df["neg"]
    # Derive the 'lowest ppm' and associated 'Inferred Max Intensity'
    df["lowest Delta ppm"] = np.where(df[diff] == df["min_ppm"], df[diff], np.nan)
    df["Intensity"] = np.where(df[diff] == df["min_ppm"], df[intensity], np.nan)
    # Remove temporary variables and sort (NaN > anything else)
    df["abs_diff"] = df[diff].abs()
    df["has_inferred_structure"] = np.where(df[inferred_structure].notna(), 1, 2)
    df["has_ppm"] = np.where(df["lowest Delta ppm"].notna(), 1, 2)
    df.sort_values(
        by=[
            "has_inferred_structure",
            observed_id,
            "has_ppm",
            "min_abs_diff",
        ],
        inplace=True,
        ascending=[True, True, True, False],
    )
    df.drop(
        [
            "neg",
            "min_abs_diff",
            "min_ppm",
            "abs_diff",
            "has_inferred_structure",
            "has_ppm",
        ],
        axis=1,
        inplace=True,
    )
    # Convert data types
    df = df.convert_dtypes()
    return df
