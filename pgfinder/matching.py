"""Matching functions"""
import logging
from decimal import *
from pgfinder import MULTIMERS, MOD_TYPE, MASS_TO_CLEAN
import pandas as pd

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


def filtered_theo(ftrs_df: pd.DataFrame, theo_list: pd.DataFrame, user_ppm: int) -> pd.DataFrame:
    """Generate list of observed structures from theoretical masses dataframe to reduce search space.

    Parameters
    ----------
    ftrs_df: pd.DataFrame
        Features dataframe.
    theo_list: pd.DataFrame
        Theoretical dataframe.
    user_ppm: int

    Returns
    -------
    pd.DataFrame
        ?
    """
    # Match theoretical structures to raw data to generate a list of observed structures
    matched_df = matching(ftrs_df, theo_list, user_ppm)

    # Create dataframe containing only theo_mwMonoisotopic & inferredStructure columsn from matched_df
    filtered_df = matched_df.filter(["inferredStructure","theo_mwMonoisotopic"], axis=1)

    # Drop all rows with NaN values in the theo_mwMonoisotopic column
    filtered_df.dropna(subset=["theo_mwMonoisotopic"], inplace=True)

    # Drop duplicate structures and masses
    filtered_df.drop_duplicates(inplace=True)

    filtered_df.rename(
        columns={"theo_mwMonoisotopic": "Monoisotopicmass", "inferredStructure": "Structure"}, inplace=True
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
        dataframe containing theoretical multimers and thier corresponding masses
    """

    theo_mw = []
    theo_struct = []
    # Builder sub function - calculates multimer mass and name
    # FIXME : No need to use nested functions
    def builder(name, mass, mult_num: int):
        for idx, row in theo_df.iterrows():
            if (
                len(row.Structure[: len(row.Structure) - 2]) > 2
            ):  # Prevent dimer creation using just gm (input format is XX|n) X = letters n = number
                mw = row.Monoisotopicmass
                acceptor = row.Structure[: len(row.Structure) - 2]
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
    multimer_df = pd.DataFrame(list(zip(theo_mw, theo_struct)), columns=["Monoisotopicmass", "Structure"])
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

    # FIXME : Replace with data structure such as dictionary
    mod_mass = Decimal(MOD_TYPE[mod_type]["mass"])
    mod_name = MOD_TYPE[mod_type]["name"]

    obs_theo_muropeptides_df = filtered_theo_df.copy()
    # Calculate new mass of modified structure
    obs_theo_muropeptides_df["Monoisotopicmass"] = obs_theo_muropeptides_df["Monoisotopicmass"].map(
        lambda Monoisotopicmass: Decimal(Monoisotopicmass) + mod_mass
    )

    # add modification tags to structure name
    if mod_type == "Decay":
        obs_theo_muropeptides_df["Structure"] = obs_theo_muropeptides_df["Structure"].map(
            lambda Structure: Structure[1 : len(Structure)]
        )
    elif mod_type == "Sodium" or mod_type == "Potassium":
        obs_theo_muropeptides_df["Structure"] = obs_theo_muropeptides_df["Structure"].map(
            lambda Structure: mod_name + " " + Structure
        )
    elif mod_type == "Nude":
        obs_theo_muropeptides_df["Structure"] = obs_theo_muropeptides_df["Structure"].map(
            lambda Structure: mod_name + Structure
        )
    else:
        obs_theo_muropeptides_df["Structure"] = obs_theo_muropeptides_df["Structure"].map(
            lambda Structure: Structure[: len(Structure) - 2]
            + " "
            + "("
            + mod_type
            + ")"
            + " "
            + Structure[len(Structure) - 2 : len(Structure)]
        )
    return obs_theo_muropeptides_df

def matching(ftrs_df: pd.DataFrame, matching_df: pd.DataFrame, set_ppm: int):
    molecular_weights = matching_df[["Structure", "Monoisotopicmass"]]
    matches_df = pd.DataFrame()

    for s, m in molecular_weights.itertuples(index=False):
        tolerance = calc_ppm_tolerance(m, set_ppm)
        mw_matches = ftrs_df[
            (ftrs_df["mwMonoisotopic"] >= m - tolerance) & (ftrs_df["mwMonoisotopic"] <= m + tolerance)
        ].copy()

        # If we have matches add the structure and molecular weight then append
        if len(mw_matches.index) > 0:
            mw_matches["inferredStructure"] = s
            mw_matches["theo_mwMonoisotopic"] = round(m, 4)
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
    matching_df: pd.DataFrame
        ?
    set_ppm: int
        Integer value used to calculate a upper and lower bound mass range for an observed value to be considered the same as a theoretical value

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
    parent_muropeptide_df = ftrs_df.loc[ftrs_df["inferredStructure"].str.contains(parent, na=False)]

    # Generate adduct dataframe - contains adducts
    adducted_muropeptide_df = ftrs_df.loc[ftrs_df["inferredStructure"].str.contains(target, na=False)]

    # print(parent_muropeptide_df)
    # print(adducted_muropeptide_df)

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
    for x, row in parent_muropeptide_df.iterrows():
        # Get retention time value from row
        rt = row.rt
        #Get parent structure
        parent_structure = row.inferredStructure
        #Get parent ID
        parent_ID = row.ID
        #Get parent intensity
        parent_intensity = row.maxIntensity

        # Work out rt window
        upper_lim_rt = rt + time_delta
        lower_lim_rt = rt - time_delta

        # Get all adduct enteries within rt window
        ins_constrained_df = adducted_muropeptide_df[
            adducted_muropeptide_df["rt"].between(lower_lim_rt, upper_lim_rt, inclusive="both")
        ]
        if not ins_constrained_df.empty:
            if target == "^m":
                ins_constrained_df["inferredStructure"] = "g" + ins_constrained_df["inferredStructure"].astype(str)
            if target == "^Na+":
                ins_constrained_df["inferredStructure"] =  ins_constrained_df["inferredStructure"].str.replace("Na\+ ", "")
            if target == "^K+":
                ins_constrained_df["inferredStructure"] =  ins_constrained_df["inferredStructure"].str.replace("K\+ ", "")

        for y, ins_row in ins_constrained_df.iterrows():
            ins_structure = ins_row.inferredStructure
            ins_intensity = ins_row.maxIntensity
            if parent_structure == ins_structure:
                #Get index to value to consolidate
                idx = consolidated_decay_df.loc[consolidated_decay_df["inferredStructure"] == parent_structure].index[0]
                #consolidate intensity value
                consolidated_decay_df.at[idx, "maxIntensity"] = parent_intensity + ins_intensity
                #get index of target to drop
                drop_idx = ins_constrained_df.loc[ins_constrained_df["inferredStructure"] == ins_structure].index[0]
                #Drop target row
                consolidated_decay_df.drop(drop_idx, inplace=True)

    return consolidated_decay_df

def data_analysis(
    raw_data_df: pd.DataFrame, theo_masses_df: pd.DataFrame, rt_window: float, enabled_mod_list: list, user_ppm=int,
long_format: bool = False) -> pd.DataFrame:
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
    obs_monomers_df = filtered_theo(ff, theo, user_ppm)
    # print(obs_monomers_df.dtypes)
    # print(obs_monomers_df.head)

    # FIXME : Is this the logic that is required? It seems only one type of multimers will ever get built but is it not
    #         possible that there are multiple types listed in the enbaled_mod_list?
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
    obs_frames = [obs_monomers_df, obs_multimers_df]
    obs_theo_df = pd.concat(obs_frames).reset_index(drop=True)

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
    master_frame = master_frame.astype({"Monoisotopicmass": float})
    LOGGER.info("Matching")
    matched_data_df = matching(ff, master_frame, user_ppm)
    LOGGER.info("Cleaning data")


    cleaned_df = clean_up(ftrs_df=matched_data_df, mass_to_clean=sodium, time_delta=time_delta_window)
    cleaned_df = clean_up(ftrs_df=cleaned_df, mass_to_clean=potassium, time_delta=time_delta_window)
    cleaned_data_df = clean_up(ftrs_df=cleaned_df, mass_to_clean=sugar, time_delta=time_delta_window)
    cleaned_data_df.sort_values("inferredStructure", inplace=True, ascending=True)

    # set metadata
    cleaned_data_df.attrs["file"] = raw_data_df.attrs["file"]
    cleaned_data_df.attrs["masses_file"] = theo_masses_df.attrs["file"]
    cleaned_data_df.attrs["rt_window"] = rt_window
    cleaned_data_df.attrs["modifications"] = enabled_mod_list
    cleaned_data_df.attrs["ppm"] = user_ppm

    return cleaned_data_df
