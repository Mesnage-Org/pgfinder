import pandas as pd
import sqlite3
import numpy as np
from decimal import *



def calc_ppm_tolerance(mw: float, ppm_tol: int = 10):
    '''
    Calculates ppm tolerance value
    :param mw:
    :param ppm_tol:
    :return float:
    '''
    return (mw * ppm_tol) / 1000000


def filtered_theo(ftrs_df, theo_list, user_ppm: int):
    '''
    Generate list of observed structures from theoretical masses dataframe to reduce search space

    :param ftrs_df:
    :param theo_list:
    :param user_ppm:
    :return dataframe:
    '''

    matched_df = matching(ftrs_df,theo_list,user_ppm) # Match theoretical structures to raw data to generate a list of observed structures

    filtered_df = matched_df.loc[:, 'theo_mwMonoisotopic':'inferredStructure'] # Create dataframe containing only theo_mwMonoisotopic & inferredStructure columsn from matched_df
    filtered_df.dropna(subset=['theo_mwMonoisotopic'], inplace=True) # Drop all rows with NaN values in the theo_mwMonoisotopic column

    #Explode dataframe so each inferred structure has its own row and corresponding theo_mwMonoisotopic value
    cols = ['theo_mwMonoisotopic', 'inferredStructure']
    exploded_df = pd.concat([filtered_df[col].str.split(',', expand=True) for col in cols], axis=1, keys=cols).stack().reset_index(level=1, drop=True)
    exploded_df.drop_duplicates(subset='inferredStructure', keep='first', inplace=True)

    exploded_df.rename(columns={'theo_mwMonoisotopic': 'Monoisotopicmass', 'inferredStructure': 'Structure'},
                       inplace=True)

    return exploded_df


def multimer_builder(theo_list, multimer_type: int = 0):
    '''
    Generate multimers (dimers & trimers) from observed monomers
    :param theo_list:
    :param multimer_type:
    :return dataframe:
    '''

    theo_mw = []
    theo_struct = []
#Builder sub function - calculates multimer mass and name

    def builder(name, mass, mult_num: int):
        for idx, row in theo_list.iterrows():
            if len(row.Structure[:len(row.Structure)-2]) > 2: #Prevent dimer creation using just GM (input format is XX|n) X = letters n = number
                mw = row.Monoisotopicmass
                acceptor = row.Structure[:len(row.Structure)-2]
                donor = name
                donor_mw = mass
                theo_mw.append(Decimal(mw)+donor_mw+Decimal('-18.0106'))
                theo_struct.append(acceptor+'-'+donor+'|'+str(mult_num))

# Calls builder subfunction with different arguements based on multimer type selected

    # Calculates multimers based on peptide bond through side chain
    if multimer_type == 0:
        builder("GM-AEJA", Decimal('941.4075'), 2)
        builder("GM-AEJ", Decimal('870.3704'), 2)
        builder("GM-AEJ-GM-AEJ", Decimal('1722.7302'), 3)
        builder("GM-AEJ-GM-AEJA", Decimal('1793.7673'), 3)
        builder("GM-AEJA-GM-AEJA", Decimal('1864.8044'), 3)

    # Calculates multimers based on glycosidic bond through dissachrides & peptide bonds through side chains
    elif multimer_type == 1:
        builder("GM-AE", Decimal('698.2858'), 2)
        builder("GM-AEJA", Decimal('941.4075'), 2)
        builder("GM-AEJ", Decimal('870.3704'), 2)
        builder("GM-AEJ-GM-AEJ", Decimal('1722.7302'), 3)
        builder("GM-AEJ-GM-AEJA", Decimal('1793.7673'), 3)
        builder("GM-AEJA-GM-AEJA", Decimal('1864.8044'), 3)

        builder("GM-AEJA_(Glyco)",  Decimal('939.3919'), 2)
        builder("GM-AEJ_(Glyco)", Decimal('868.3548'), 2)
        builder("GM-AEJ-GM-AEJ_(Glyco)",  Decimal('1720.7146'), 3)
        builder("GM-AEJ-GM-AEJA_(Glyco)",  Decimal('1791.7517'), 3)
        builder("GM-AEJA-GM-AEJA_(Glyco)",  Decimal('1862.7888'), 3)

    # Calculates multimers based on Lactyl peptides (peptide bond via side chain but no dissachrides on muropeptides)
    elif multimer_type == 2:
        builder("Lac-AEJA",  Decimal('533.2333'), 2)
        builder("Lac-AEJ",  Decimal('462.1962'), 2)
        builder("Lac-AEJ-Lac-AEJ",  Decimal('906.3818'), 3)
        builder("Lac-AEJ-Lac-AEJA",  Decimal('977.4189'), 3)
        builder("Lac-AEJA-Lac-AEJA", Decimal('1048.4560'), 3)

    # converts lists to dataframe
    multimer_df = pd.DataFrame(list(zip(theo_mw, theo_struct)), columns=['Monoisotopicmass', 'Structure'])

    return multimer_df


def modification_generator(filtered_theo_df, mod_type: str):
    '''
    Generates modified muropeptides (calculates new mass and add modification tag to structure name)
    :param filtered_theo_df:
    :param mod_type:
    :return dataframe:
    '''

    if mod_type == "Anhydro":
        mod_mass = Decimal('-20.0262')
    elif mod_type == "Double Anhydro":
        mod_mass = Decimal('-40.0524')
    elif mod_type == "Deacetyl":
        mod_mass = Decimal('-42.0105')
    elif mod_type == "O-Acetylated":
        mod_mass = Decimal('42.0105')
    elif mod_type == "Deacetyl-Anhydro":
        mod_mass = Decimal('-62.0368')
    elif mod_type == "Decay":
        mod_mass = Decimal('-203.0793')
    elif mod_type == "Sodium":
        mod_mass = Decimal('21.9819')
        mod_name = "Na+"
    elif mod_type == 'Potassium':
        mod_mass = Decimal('37.9559')
        mod_name = "K+"
    elif mod_type == "Nude":
        mod_mass = Decimal('478.1799')
        mod_name = "GM-"
    elif mod_type == "Amidated":
        mod_mass = Decimal('-0.9840')
        mod_name = "Amidated"
    elif mod_type == "Amidase Product":
        mod_mass = Decimal('-480.1955')
        mod_name = "(Amidase Product)"
    elif mod_type == "Lactyl":
        mod_mass = Decimal('-408.1744')
        mod_name = "(Lactyl)"

    obs_theo_muropeptides_df = filtered_theo_df.copy()
    # Calculate new mass of modified structure
    obs_theo_muropeptides_df['Monoisotopicmass'] = obs_theo_muropeptides_df['Monoisotopicmass'].map(
        lambda Monoisotopicmass: Decimal(Monoisotopicmass) + mod_mass)

# add modification tags to structure name
    if mod_type == "Decay":
        obs_theo_muropeptides_df['Structure'] = obs_theo_muropeptides_df['Structure'].map(
            lambda Structure: Structure[1:len(Structure)])
    elif mod_type == "Sodium" or mod_type == "Potassium":
        obs_theo_muropeptides_df['Structure'] = obs_theo_muropeptides_df['Structure'].map(
            lambda Structure: mod_name + " " + Structure)
    elif mod_type == 'Nude':
        obs_theo_muropeptides_df['Structure'] = obs_theo_muropeptides_df['Structure'].map(
            lambda Structure: mod_name + Structure)
    else:
        obs_theo_muropeptides_df['Structure'] = obs_theo_muropeptides_df['Structure'].map(
            lambda Structure:  Structure[:len(Structure)-2] + " " + "(" + mod_type + ")" + " " + Structure[len(Structure)-2:len(Structure)])

    return obs_theo_muropeptides_df


def matching(ftrs_df: pd.DataFrame, matching_df: pd.DataFrame, set_ppm: int):
    '''
    Match theoretical masses to observed masses within ppm tolerance.
    :param ftrs_df:
    :param matching_df:
    :param set_ppm:
    :return raw_data - dataframe:
    '''

    raw_data = ftrs_df.copy()
    #Data validation
    if ('Monoisotopicmass' not in matching_df.columns) | ('Structure' not in matching_df.columns):
        print(
            'Header of csv files must have column named "Monoisotopic mass" and another column named "Structure"!!!  Make note of capitalized letters and spacing!!!!')
# Generates dataframe with matched structures
    for x, row in raw_data.iterrows():
        # Observed monoisotopic mass
        mw = row.mwMonoisotopic
        # ppm tolerance value
        t_tol = calc_ppm_tolerance(mw, set_ppm)
        # create dataframe with values from matching_df within tolerance to observed monoisotopic mass
        t_df = matching_df[(matching_df['Monoisotopicmass'] >= mw - t_tol) & (matching_df['Monoisotopicmass'] <= mw + t_tol)]

        # Populate inferred structure and theo_mwMonoisotopic columns with matched values
        if not t_df.empty:
            raw_data.loc[x, "inferredStructure"] = ','.join(t_df.Structure.values)
            raw_data.loc[x, "theo_mwMonoisotopic"]= ','.join(map(str, t_df.Monoisotopicmass.values))


    return raw_data


def clean_up(ftrs_df, mass_to_clean: Decimal, time_delta: float):

    # Mass values for adducts
    sodiated = Decimal('21.9819')
    potassated = Decimal('37.9559')
    decay = Decimal('203.0793')
    
    # Selector substrings for generating parent and adduct dataframes
    if mass_to_clean == sodiated:
        parent = "^GM|^M|^Lac"
        target = "^Na+"
    elif mass_to_clean == potassated:
        parent = "^GM|^M|^Lac"
        target = "^K+"
    elif mass_to_clean == decay:
        parent = "^GM"
        target = "^M"

    # Generate parent dataframe - contains parents
    parent_muropeptide_df = ftrs_df[
        ftrs_df['inferredStructure'].str.contains(parent, na=False)] 
    
    # Generate adduct dataframe - contains adducts 
    adducted_muropeptide_df = ftrs_df[
        ftrs_df['inferredStructure'].str.contains(target, na=False)]  
    
    # Generate copy of rawdata dataframe
    consolidated_decay_df = ftrs_df.copy()

    # Status updates (prints to console)
    if parent_muropeptide_df.empty:
        print("No ", parent ," muropeptides found")
    if adducted_muropeptide_df.empty:
        print("No ", target ," found")
    elif mass_to_clean == sodiated:
        print("Processing", adducted_muropeptide_df.size, "Sodium Adducts")
    elif mass_to_clean == potassated:
        print("Processing", adducted_muropeptide_df.size, "potassium adducts")
    elif mass_to_clean == decay:
        print("Processing", adducted_muropeptide_df.size, "in source decay products")

    # Consolidate adduct intensity with parent ions intensity
    for y, row in parent_muropeptide_df.iterrows():
        # Get retention time value from row
        rt = row.rt
        # Get theoretical monoisotopic mass value from row as list of values
        intact_mw = list(str(row.theo_mwMonoisotopic).split(','))

        # Work out rt window
        upper_lim_rt = rt + time_delta
        lower_lim_rt = rt - time_delta
        
        # Get all adduct enteries within rt window
        ins_constrained_df = adducted_muropeptide_df[adducted_muropeptide_df['rt'].between(lower_lim_rt, upper_lim_rt,
                                                                                           inclusive='both')]

        
        if not ins_constrained_df.empty:

            for z, ins_row in ins_constrained_df.iterrows():
                ins_mw = list(str(ins_row.theo_mwMonoisotopic).split(","))
                
                # Compare parent masses to adduct masses
                for mass in intact_mw:
                    for mass_2 in ins_mw:

                        mass_delta = abs(
                            Decimal(mass).quantize(Decimal('0.00001')) - Decimal(mass_2).quantize(Decimal('0.00001')))
                        
                        # Consolidate intensities
                        if mass_delta == mass_to_clean:

                            consolidated_decay_df.sort_values('ID', inplace=True, ascending=True)

                            insDecay_intensity = ins_row.maxIntensity
                            parent_intensity = row.maxIntensity
                            consolidated_intensity = insDecay_intensity + parent_intensity

                            ID = row.ID
                            drop_ID = ins_row.ID

                            idx = consolidated_decay_df.loc[consolidated_decay_df['ID'] == ID].index[0]
                            try:
                                drop_idx = consolidated_decay_df.loc[consolidated_decay_df['ID'] == drop_ID].index[0]
                                consolidated_decay_df.at[idx, 'maxIntensity'] = consolidated_intensity
                                consolidated_decay_df.drop(drop_idx, inplace=True)
                            except IndexError:
                                print("drop idx: ", drop_idx, " has already been removed")

    return consolidated_decay_df


def ftrs_reader(filePath: str):
    '''
    Reads FTRS file from Byos
    :param filePath:
    :return dataframe:
    '''

    with sqlite3.connect(filePath) as db:

        sql = "SELECT * FROM Features"
        #Reads sql database into dataframe
        ff = pd.read_sql(sql, db)
        # adds inferredStructure column
        ff['inferredStructure'] = np.nan
        # adds theo_mwMonoisotopic column
        ff['theo_mwMonoisotopic'] = np.nan
        # Renames columns to expected column heading required for data_analysis function
        ff.rename(columns={'Id': 'ID', 'apexRetentionTimeMinutes': 'rt', 'apexMwMonoisotopic': 'mwMonoisotopic', 'maxAveragineCorrelation': 'corrMax' }, inplace=True)
        # Desired column order
        cols_order = ['ID', 'xicStart', 'xicEnd', 'feature', 'corrMax', 'ionCount', 'chargeOrder', 'maxIsotopeCount',
                      'rt', 'mwMonoisotopic','theo_mwMonoisotopic', 'inferredStructure', 'maxIntensity', ]
        # Reorder columns in dataframe to desired order.
        ff = ff[cols_order]

        return ff


def maxquant_file_reader(filepath: str):
    '''
        Reads maxquant files and outputs data as a dataframe

    :param filepath (file should be a text file):
    :return dataframe:
    '''

    # reads file into dataframe
    maxquant_df = pd.read_table(filepath, low_memory=False)
    # adds inferredStructure column
    maxquant_df['inferredStructure'] = np.nan
    # adds theo_mwMonoisotopic column
    maxquant_df['theo_mwMonoisotopic'] = np.nan
    # insert dataframe index as a column
    maxquant_df.reset_index(level=0, inplace=True)
    # Renames columns to expected column heading required for data_analysis function
    maxquant_df.rename(columns={'index': 'ID','Retention time': 'rt', 'Retention length': 'rt_length',
                                'Mass': 'mwMonoisotopic', 'Intensity': "maxIntensity"},
                               inplace=True)
    # Keeps only essential columns, all extraneous columns are left out.
    focused_maxquant_df = maxquant_df[['ID', 'mwMonoisotopic', 'rt', 'rt_length', 'maxIntensity', 'inferredStructure',
                                       'theo_mwMonoisotopic']]
    # Desired column order
    cols_order = ['ID', 'rt', 'rt_length', 'mwMonoisotopic', 'theo_mwMonoisotopic', 'inferredStructure', 'maxIntensity']
    # Reorder columns in dataframe to desired order.
    focused_maxquant_df = focused_maxquant_df[cols_order]


    return focused_maxquant_df


def theo_masses_reader(filepath: str):

    '''
    Reads theoretical masses files (csv)
    :param filepath:
    :return dataframe:
    '''
    # reads csv files and converts to dataframe
    theo_masses_df = pd.read_csv(filepath)

    return theo_masses_df


def data_analysis(raw_data_df: pd.DataFrame, theo_masses_df: pd.DataFrame, rt_window: float, enabled_mod_list: list, user_ppm = int):

    sugar = Decimal('203.0793')
    sodium = Decimal('21.9819')
    potassium = Decimal('37.9559')
    time_delta_window = rt_window #retention time window to look in for in source decay products (rt of parent ion plus or minus time_delta)




    theo = theo_masses_df
    ff = raw_data_df

    print("Filtering Theo masses by observed masses")
    obs_monomers_df = filtered_theo(ff, theo,user_ppm)

    if 'Multimers' in enabled_mod_list:
        print("Building multimers from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df)
        print("fitering theo multimers by observed")
        obs_multimers_df = filtered_theo(ff, theo_multimers_df,user_ppm)
    elif 'multimers_Glyco' in enabled_mod_list:
        print("Building multimers from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df, 1)
        print("fitering theo multimers by observed")
        obs_multimers_df = filtered_theo(ff, theo_multimers_df, user_ppm)
    elif 'Multimers_Lac' in enabled_mod_list:
        print("Building multimers_Lac from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df, 2)
        print("fitering theo multimers by observed")
        obs_multimers_df = filtered_theo(ff, theo_multimers_df, user_ppm)
    else:
        obs_multimers_df = pd.DataFrame()

    print("building custom searh file")
    obs_frames = [obs_monomers_df, obs_multimers_df]
    obs_theo_df = pd.concat(obs_frames).reset_index(drop=True)

    print("generating variants")

    if 'Sodium' in enabled_mod_list:
        adducts_sodium_df = modification_generator(obs_theo_df, "Sodium")
    else:
        adducts_sodium_df = pd.DataFrame()

    if 'Potassium' in enabled_mod_list:
        adducts_potassium_df = modification_generator(obs_theo_df, "Potassium")
    else:
        adducts_potassium_df = pd.DataFrame()

    if 'Anhydro' in enabled_mod_list:
        anhydro_df = modification_generator(obs_theo_df, "Anhydro")
    else:
        anhydro_df = pd.DataFrame()

    if 'DeAc' in enabled_mod_list:
        deacetyl_df = modification_generator(obs_theo_df, "Deacetyl")
    else:
        deacetyl_df = pd.DataFrame()

    if 'Deacetyl_Anhydro' in enabled_mod_list:
        deac_anhy_df = modification_generator(obs_theo_df, "Deacetyl-Anhydro")
    else:
        deac_anhy_df = pd.DataFrame()
    if 'O-Acetylated' in enabled_mod_list:
        oacetyl_df = modification_generator(obs_theo_df, "O-Acetylated")
    else:
        oacetyl_df = pd.DataFrame()

    if 'Nude' in enabled_mod_list:
        nude_df = modification_generator(obs_theo_df, "Nude")
    else:
        nude_df = pd.DataFrame()

    if 'Decay' in enabled_mod_list:
        decay_df = modification_generator(obs_theo_df, "Decay")
    else:
        decay_df = pd.DataFrame()

    if 'Amidation' in enabled_mod_list:
        ami_df = modification_generator(obs_theo_df,"Amidated")
    else:
        ami_df = pd.DataFrame()

    if 'Amidase' in enabled_mod_list:
        deglyco_df = modification_generator(obs_theo_df,'Amidase Product')
    else:
        deglyco_df = pd.DataFrame()

    if 'Double_Anh' in enabled_mod_list:
        double_Anhydro_df = modification_generator(obs_theo_df, 'Double Anhydro')
    else:
        double_Anhydro_df = pd.DataFrame()



    master_frame = [obs_theo_df, adducts_potassium_df, adducts_sodium_df, anhydro_df, deac_anhy_df, deacetyl_df,
                    oacetyl_df, decay_df, nude_df, ami_df, deglyco_df, double_Anhydro_df]
    master_list = pd.concat(master_frame)
    master_list = master_list.astype({'Monoisotopicmass': float})
    print("Matching")
    matched_data_df = matching(ff, master_list, user_ppm)
    print("Cleaning data")
    cleaned_df = clean_up(matched_data_df, sodium, time_delta_window)
    cleaned_df = clean_up(cleaned_df, potassium, time_delta_window)
    cleaned_data_df = clean_up(cleaned_df, sugar, time_delta_window)

    cleaned_data_df.sort_values('inferredStructure', inplace=True, ascending=True)

    return cleaned_data_df

def dataframe_to_csv(save_filepath: str, filename:str ,output_dataframe: pd.DataFrame ):
    '''
    Writes dataframe to csv file at desired file location
    :param save_filepath:
    :param filename:
    :param output_dataframe:
    :return csv file:
    '''

    #Combine save location and desired file name with correct formatting for output as csv file.
    write_location = save_filepath + '/' + filename + '.csv'
    output_dataframe.to_csv(write_location, index=False)


