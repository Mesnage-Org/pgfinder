"""Matching functions"""

import logging
import re
from decimal import Decimal

import pandas as pd
from pandas.api.types import is_numeric_dtype

from pgfinder import COLUMNS, MASS_TO_CLEAN, MOD_TYPE, MULTIMERS
from pgfinder.errors import UserError
from pgfinder.logs.logs import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME)

# Only need pgfinder columns so subset those here to simplify subsequent indexing
COLUMNS = COLUMNS["pgfinder"]


def calc_ppm_tolerance(mw: float, ppm_tol: int = 10) -> float:
    """
    Calculates ppm tolerance value

    Parameters
    ----------
    mw : float
        Molecular weight.
    ppm_tol : int
        PPM tolerance

    Returns
    -------
    float
        ?
    """
    return (mw * ppm_tol) / 1000000


def filtered_theo(ftrs_df: pd.DataFrame, theo_df: pd.DataFrame, user_ppm: int) -> pd.DataFrame:
    """
    Generate list of observed structures from theoretical masses dataframe to reduce search space.

    Parameters
    ----------
    ftrs_df : pd.DataFrame
        Features dataframe.
    theo_df : pd.DataFrame
        Theoretical dataframe.
    user_ppm : int
        User specified Parts Per Million.

    Returns
    -------
    pd.DataFrame
        Dataframe filtered on matches with theoretical masses.
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
        raise UserError("No matches were found for this search. Please check your database or increase mass tolerance.")

    return filtered_df


def multimer_builder(theo_df: pd.DataFrame, multimer_type: str, columns: dict = COLUMNS) -> pd.DataFrame:
    """
    Generate multimers (dimers & trimers) from observed monomers.

    Parameters
    ----------
    theo_df : pd.DataFrame
        Dataframe containing theoretical monomerics structures and their corresponding masses.
    multimer_type : str
        Type of multimers to build.
    columns : dict
        Dictionary of pgfinder columns, loaded by default from 'pgfinder/config/columns.yaml'.

    Returns
    -------
    pd.DataFrame
        Dataframe containing theoretical multimers and their corresponding masses.
    """

    theo_mw = []
    theo_struct = []

    # Perhaps need a better way
    inferred_structure = columns["inferred"]["structure"]

    # Builder sub function - calculates multimer mass and name
    def builder(name, mass, mult_num: int):
        for _, row in theo_df.iterrows():
            if (
                len(row[inferred_structure][: len(row[inferred_structure]) - 2]) > 2
            ):  # Prevent dimer creation using just gm (input format is XX|n) X = letters n = number
                mw = row["Theo (Da)"]
                acceptor = row[inferred_structure][: len(row[inferred_structure]) - 2]
                donor = name
                donor_mw = mass
                theo_mw.append(Decimal(mw) + donor_mw + Decimal("-18.0106"))
                # FIXME: In an ideal world, `-` should actually be `~` here, but Excel will throw
                # a hissy-fit about `~` being an escape character, so that's out of scope for now
                joiner = "-" if "Glycosidic" in multimer_type else "="
                theo_struct.append(acceptor + joiner + donor + "|" + str(mult_num))

    # Call builder subfunction with different arguements based on multimer type selected
    # and calculate multimers based on peptide bond through side chain
    multimer = MULTIMERS[multimer_type]
    LOGGER.info(f"Building features for multimer type : {multimer_type}")
    [builder(molecule, Decimal(features["mass"]), features["mult_num"]) for molecule, features in multimer.items()]

    # converts lists to dataframe
    multimer_df = pd.DataFrame(list(zip(theo_mw, theo_struct)), columns=list(columns["inferred"].values()))
    return multimer_df


def modification_generator(filtered_theo_df: pd.DataFrame, mod_type: str) -> pd.DataFrame:
    """
    Generate modified muropeptides (calculates new mass and add modification tag to structure name).

    Parameters
    ----------
    filtered_theo_df : pd.DataFrame
        Pandas DataFrame of theoretical masses that have been filtered.
    mod_type : str
        Modification type ???.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of ???.
    """
    mod_mass = Decimal(MOD_TYPE[mod_type]["mass"])
    # NOTE: This regex extracts the modification abbrevation from the end of its full name / type —
    # it simply extracts the bracketed expression at the end of the line
    mod_abbr = re.search(r"\(.*\)$", mod_type).group(0)

    obs_theo_muropeptides_df = filtered_theo_df.copy()
    # Calculate new mass of modified structure
    obs_theo_muropeptides_df["Theo (Da)"] = obs_theo_muropeptides_df["Theo (Da)"].map(lambda x: Decimal(x) + mod_mass)

    # Add modification tags to structure name — there are some special cases that need handling first!
    # FIXME: Kinda pointless to have a file that the user can use to define custom modifications if
    # we're going to hard-code in special cases anyways? I suppose they can still add their own as
    # long as they don't also want any sort of "special" formatting
    base_structure = obs_theo_muropeptides_df["Inferred structure"]
    # FIXME: Absolutely no validation that these structures make sense or are chemically possible —
    # even modifications like "Loss of GlcNAc" don't guarantee that a `g` character is removed from
    # the structure's name. It just chops off the first character with reckless abandon...
    # NOTE: All of these functions assume (with no guarantee) that structures begin with `gm-`
    special_cases = {
        "Extra Disaccharide (+gm)": lambda s: "gm-" + s,
        "Lactyl Peptides (Lac)": lambda s: "Lac" + s[2:],
        "Loss of Disaccharide (-gm)": lambda s: s[3:],
        "Loss of GlcNAc (-g)": lambda s: s[1:],
    }

    # The silly `len(s) - 2` rubbish here is to preserve the `|x` multimer number at the end of
    # each structure name
    def default_case(s):
        return s[: len(s) - 2] + " " + mod_abbr + s[len(s) - 2 : len(s)]

    structure_updater = special_cases.get(mod_type, default_case)

    obs_theo_muropeptides_df["Inferred structure"] = base_structure.map(structure_updater)
    return obs_theo_muropeptides_df


def matching(ftrs_df: pd.DataFrame, matching_df: pd.DataFrame, set_ppm: int) -> pd.DataFrame:
    """
    Match theoretical masses to observed masses within ppm tolerance.

    Parameters
    ----------
    ftrs_df : pd.DataFrame
        Features DataFrame
    matching_df : pd.DataFrame
        Matching DataFrame
    set_ppm : int

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
    """
    Clean up a DataFrame.

    Parameters
    ----------
    ftrs_df : pd.DataFrame
        Features dataframe?
    mass_to_clean : Decimal
        Mass to be cleaned.
    time_delta: float
        Clean up window.

    Returns
    -------
    pd.DataFrame:
        Tidied Dataframe.
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
    ppm_tolerance: float,
    consolidation_ppm: float,
) -> pd.DataFrame:
    """
    Perform analysis.

    Parameters
    ----------
    raw_data_df : pd.DataFrame
        User data as Pandas DataFrame.
    theo_masses_df : pd.DataFrame
        Theoretical masses as Pandas DataFrame.
    rt_window : float
        Set time window for in-source decay and salt adduct cleanup.
    enabled_mod_list : list
        List of modifications to enable.
    ppm_tolerance : float
        The ppm tolerance used when matching the theoretical masses of structures to observed ions.
    consolidation_ppm : float
        The minimum absolute ppm difference between two matches before one is picked as "most likely" over the other.

    Returns
    -------
    pd.DataFrame
        Dataframe of matches.
    """
    sugar = Decimal("203.0793")
    sodium = Decimal("21.9819")
    potassium = Decimal("37.9559")

    LOGGER.info("Filtering theoretical masses by observed masses")
    obs_monomers_df = filtered_theo(ftrs_df=raw_data_df, theo_df=theo_masses_df, user_ppm=ppm_tolerance)
    # Make sure the enabled_mod_list (if empty), is actually represented by an empty list
    enabled_mod_list = enabled_mod_list or []

    # NOTE: "Multimers" is a semi-magic keyword here. Multimers and modifications are treated
    # differently by most of the code and have their own sections in `parameters.yaml`, but
    # despite this, all of the multimer and modification flags are passed to `data_analysis()`
    # in the same `enabled_mod_list` variable... This is the shortest path to getting something
    # working now.
    multimer_mods = [m for m in enabled_mod_list if "Multimers" in m]
    other_mods = [m for m in enabled_mod_list if m not in multimer_mods]

    def build_multimers(mod):
        LOGGER.info("Building multimers from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df, mod)
        LOGGER.info("Filtering theoretical multimers by observed")
        return filtered_theo(raw_data_df, theo_multimers_df, ppm_tolerance)

    obs_theo_df = pd.concat([obs_monomers_df, *(build_multimers(type) for type in multimer_mods)])

    def apply_modification(mod):
        LOGGER.info(f"Generating {mod} variants")
        return modification_generator(obs_theo_df, mod)

    LOGGER.info("Building custom search file")
    master_frame = pd.concat(
        [
            obs_theo_df,
            *(apply_modification(mod) for mod in other_mods),
        ]
    )

    master_frame = master_frame.astype({"Theo (Da)": float})
    LOGGER.info("Matching")
    matched_data_df = matching(raw_data_df, master_frame, ppm_tolerance)
    LOGGER.info("Cleaning data")

    matched_data_df = calculate_ppm_delta(df=matched_data_df)

    cleaned_df = clean_up(ftrs_df=matched_data_df, mass_to_clean=sodium, time_delta=rt_window)
    cleaned_df = clean_up(ftrs_df=cleaned_df, mass_to_clean=potassium, time_delta=rt_window)
    cleaned_data_df = clean_up(ftrs_df=cleaned_df, mass_to_clean=sugar, time_delta=rt_window)

    cleaned_data_df.sort_values(by=["Intensity", "RT (min)"], ascending=[False, True], inplace=True, kind="stable")
    cleaned_data_df.reset_index(drop=True, inplace=True)

    # Apply some post-processing to the results
    most_likely_df = pick_most_likely_structures(cleaned_data_df, consolidation_ppm)
    final_df = consolidate_results(most_likely_df)

    # set metadata
    final_df.attrs["file"] = raw_data_df.attrs["file"]
    final_df.attrs["masses_file"] = theo_masses_df.attrs["file"]
    final_df.attrs["rt_window"] = rt_window
    final_df.attrs["modifications"] = enabled_mod_list
    final_df.attrs["ppm"] = ppm_tolerance
    final_df.attrs["consolidation_ppm"] = consolidation_ppm

    return final_df


def calculate_ppm_delta(
    df: pd.DataFrame,
    observed: str = COLUMNS["input"]["obs"],
    theoretical: str = COLUMNS["inferred"]["mass"],
    diff: str = COLUMNS["delta"],
) -> pd.DataFrame:
    """
    Calculate the difference in Parts Per Million between observed and theoretical masses.

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


def pick_most_likely_structures(
    df: pd.DataFrame,
    consolidation_ppm: float,
    columns: dict = COLUMNS,
) -> pd.DataFrame:
    """
    Add rows that consolidate ambiguous matches, picking matches with the closest ppm.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of structures to be processed.
    consolidation_ppm : float
        Minimum Parts Per Million tolerance distinguishing matches.
    columns : dict
        Dictionary of columns, this defaults to the global COLUMNS which is read from 'config/columns.yaml' and
    simplifies extension to new formats.

    Returns
    -------
    pd.DataFrame
        Dataframe of matches within the specified tolerance. Candidates that are not matched are included
        in the file for completeness.
    """

    def add_most_likely_structure(group) -> pd.DataFrame:
        """
        Determines the most likely structure.

        Parameters
        ----------
        group : pd.DataFrame
            DataFrame of structures.

        Returns
        -------
        pd.DataFrame
            Dataframe of most likely values.
        """
        # Sort by lowest absolute ppm first, then break ties with structures (short to long)
        group.sort_values(
            by=[columns["delta"], columns["inferred"]["structure"]],
            ascending=[True, False],
            key=lambda k: abs(k) if is_numeric_dtype(k) else k,
            inplace=True,
            kind="stable",
        )
        group.reset_index(drop=True, inplace=True)

        abs_min_ppm = group[columns["delta"]].loc[0]
        abs_min_intensity = group[columns["input"]["intensity"]].loc[0]

        min_ppm_structure_idxs = abs(abs(abs_min_ppm) - abs(group[columns["delta"]])) < consolidation_ppm
        min_ppm_structures = ",   ".join(group[columns["inferred"]["structure"]].loc[min_ppm_structure_idxs])

        group.at[0, f"Inferred structure ({columns['best_match_suffix']})"] = min_ppm_structures
        group.at[0, f"Intensity ({columns['best_match_suffix']})"] = abs_min_intensity

        return group

    matched_rows = df[df[columns["inferred"]["structure"]].notnull()]
    unmatched_rows = df[df[columns["inferred"]["structure"]].isnull()]

    grouped_df = matched_rows.groupby("ID", as_index=False, sort=False)
    most_likely = grouped_df.apply(add_most_likely_structure)

    merged_df = pd.concat([most_likely, unmatched_rows])

    return merged_df.reset_index(drop=True)


def consolidate_results(
    df: pd.DataFrame,
    intensity_column: str = f"Intensity ({COLUMNS['best_match_suffix']})",
    structure_column: str = f"Inferred structure ({COLUMNS['best_match_suffix']})",
    rt_column: str = COLUMNS["input"]["rt"],
    theo_column: str = COLUMNS["inferred"]["mass"],
    ppm_column: str = COLUMNS["delta"],
    abundance_column: str = COLUMNS["consolidation"]["Abundance (%)"],
    oligomer_column: str = "Oligomerisation",
    total_column: str = COLUMNS["consolidation"]["Total Intensity"],
    columns: dict = COLUMNS,
) -> pd.DataFrame:
    """
    Add a final table of muropeptide structures and their relative abundances

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of structures to be processed.
    intensity_column : str
        Intensity column.
    structure_column : str
        Structure column.
    rt_column : str
        RT column.
    theo_column : str
        Theoretical Mass column.
    ppm_column : str
        Delta ppm column.
    abundance_column : str
        Abundance column.
    oligomer_column : str
        Oligomer column.
    total_column : str
        Total column.

    Returns
    -------
    pd.DataFrame
        The input dataframe with additional columns containing the consolidated results.
    """

    def pick_from_highest_intensity_instance(column: pd.Series):
        return column[df.loc[column.index, intensity_column].idxmax()]

    consolidated_df = (
        df.groupby(structure_column)
        .agg(
            {
                rt_column: pick_from_highest_intensity_instance,
                intensity_column: "sum",
                theo_column: pick_from_highest_intensity_instance,
                ppm_column: pick_from_highest_intensity_instance,
            }
        )
        .reset_index()
    )
    total_intensity = consolidated_df[intensity_column].sum()
    consolidated_df[abundance_column] = consolidated_df[intensity_column] / total_intensity * 100

    consolidated_df[oligomer_column] = consolidated_df[structure_column].apply(lambda s: s[-1])
    consolidated_df.sort_values(
        by=[oligomer_column, abundance_column], ascending=[True, False], inplace=True, kind="stable", ignore_index=True
    )

    consolidated_df.at[0, total_column] = total_intensity
    consolidated_df = consolidated_df[
        [total_column, structure_column, abundance_column, rt_column, theo_column, ppm_column]
    ]

    consolidated_df[rt_column] = consolidated_df[rt_column].round(2)
    consolidated_df[ppm_column] = consolidated_df[ppm_column].round(1)
    # Rename columns using mapping defined in pgfinder/config/columns.yaml under 'consolidation'
    consolidated_df.rename(columns=columns["consolidation"], inplace=True)

    return pd.concat([df, consolidated_df], axis=1)
