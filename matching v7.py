import pandas as pd
import sqlite3
import numpy as np
from decimal import *
import sys


def calc_ppm_tolerance(mw: float, ppm_tol: int = 10):
    return (mw * ppm_tol) / 1000000

def filtered_theo(ftrs_df,theo_list):

    matched_df = matching(ftrs_df,theo_list) # Match theoretical structures to raw data to generate a list of observed structures

    filtered_df = matched_df.loc[:, 'theo_mwMonoisotopic':'inferredStructure'] # Create dataframe containing only theo_mwMonoisotopic & inferredStructure columsn from matched_df
    filtered_df.dropna(subset=['theo_mwMonoisotopic'], inplace=True) # Drop all rows with NaN values in the theo_mwMonoisotopic column

    #Explode dataframe so each inferred structure has its own row and corresponding theo_mwMonoisotopic value
    cols = ['theo_mwMonoisotopic', 'inferredStructure']
    exploded_df = pd.concat([filtered_df[col].str.split(',', expand=True) for col in cols], axis=1, keys=cols).stack().reset_index(level=1, drop=True)
    exploded_df.drop_duplicates(subset='inferredStructure', keep='first', inplace=True)

    exploded_df.rename(columns={'theo_mwMonoisotopic': 'Monoisotopicmass', 'inferredStructure': 'Structure'},
                       inplace=True)

    return exploded_df

def multimer_builder(theo_list):


    theo_mw = []
    theo_struct = []

    def builder(name,mass,mult_num:int):
        for idx, row in theo_list.iterrows():
            if len(row.Structure[:len(row.Structure)-2]) > 2: #Prevent dimer creation using just GM (input format is XX|n) X = letters n = number
                mw = row.Monoisotopicmass
                acceptor = row.Structure[:len(row.Structure)-2]
                donor = name
                donor_mw = mass
                theo_mw.append(Decimal(mw)+donor_mw+Decimal('-18.0106'))
                theo_struct.append(donor+'-'+acceptor+'|'+str(mult_num))

    builder("GM-AEJA",Decimal('941.4077'),2)
    builder("GM-AEJ",Decimal('871.3706'),2)
    builder("GM-AEJ-GM-AEJ",Decimal('1722.7306'),3)
    builder("GM-AEJ-GM-AEJA",Decimal('1793.7677'),3)
    builder("GM-AEJA-GM-AEJA",Decimal('1864.8084'),3)

    multimer_df = pd.DataFrame(list(zip(theo_mw, theo_struct)), columns=['Monoisotopicmass', 'Structure'])

    return multimer_df

def modification_generator(filtered_theo_df, mod_type:str,):

    if mod_type == "Anhydro":
        mod_mass = Decimal('-20.0262')
    elif mod_type == "Deacetyl":
        mod_mass = Decimal('-42.0106')
    elif mod_type == "Deacetyl-Anhydro":
        mod_mass = Decimal('-62.0368')
    elif mod_type == "Decay":
        mod_mass = Decimal('-203.0794')
    elif mod_type == "Sodium":
        mod_mass = Decimal('21.9819')
        mod_name = "Na+"
    elif mod_type == 'Potassium':
        mod_mass = Decimal('37.9559')
        mod_name = "K+"
    elif mod_type == "Nude":
        mod_mass = Decimal('478.1799')
        mod_name = "GM-"

    obs_theo_muropeptides_df = filtered_theo_df.copy()

    obs_theo_muropeptides_df['Monoisotopicmass'] = obs_theo_muropeptides_df['Monoisotopicmass'].map(
        lambda Monoisotopicmass: Decimal(Monoisotopicmass) + mod_mass)

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

def matching(ftrs_df:pd.DataFrame,matching_df:pd.read_csv):

    raw_data = ftrs_df.copy()

    if ('Monoisotopicmass' not in matching_df.columns) | ('Structure' not in matching_df.columns):
        print(
            'Header of csv files must have column named "Monoisotopic mass" and another column named "Structure"!!!  Make note of capitalized letters and spacing!!!!')

    for x, row in raw_data.iterrows():
        mw = row.mwMonoisotopic
        t_tol = calc_ppm_tolerance(mw)
        t_df = matching_df[(matching_df['Monoisotopicmass'] >= mw - t_tol) & (matching_df['Monoisotopicmass'] <= mw + t_tol)]

        if not t_df.empty:
            raw_data.loc[x, "inferredStructure"] = ','.join(t_df.Structure.values)
            raw_data.loc[x, "theo_mwMonoisotopic"]= ','.join(map(str, t_df.Monoisotopicmass.values))


    return raw_data

def clean_up(ftrs_df, mass_to_clean:Decimal, time_delta:float):

    sodiated = Decimal('21.9819')
    potassated = Decimal('37.9559')
    decay = Decimal('203.0794')

    if mass_to_clean == sodiated:
        parent = "^GM|^M"
        target = "^Na+"
    elif mass_to_clean == potassated:
        parent = "^GM|^M"
        target = "^K+"
    elif mass_to_clean == decay:
        parent = "^GM"
        target = "^M"

    parent_muropeptide_df = ftrs_df[
        ftrs_df['inferredStructure'].str.contains(parent, na=False)]  # Get all non salt adducted muropeptide
    adducted_muropeptide_df = ftrs_df[
        ftrs_df['inferredStructure'].str.contains(target, na=False)]  # Get all salt adducted muropetides
    consolidated_decay_df = ftrs_df.copy()

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

    for y, row in parent_muropeptide_df.iterrows():
        rt = row.rt
        intact_mw = list(str(row.theo_mwMonoisotopic).split(','))
        # Work out rt window
        upper_lim_rt = rt + time_delta
        lower_lim_rt = rt - time_delta

        ins_constrained_df = adducted_muropeptide_df[adducted_muropeptide_df['rt'].between(lower_lim_rt, upper_lim_rt,
                                                                                           inclusive=True)]  # Get all enteries within rt window

        if not ins_constrained_df.empty:

            for z, ins_row in ins_constrained_df.iterrows():
                ins_mw = list(str(ins_row.theo_mwMonoisotopic).split(","))

                for mass in intact_mw:
                    for mass_2 in ins_mw:

                        mass_delta = abs(
                            Decimal(mass).quantize(Decimal('0.00001')) - Decimal(mass_2).quantize(Decimal('0.00001')))

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

def main(ftrs_filePath:str, csv_filepath:str):

    sugar = Decimal('203.0794')
    sodium = Decimal('21.9819')
    potassium = Decimal('37.9559')
    time_delta_window = 0.08 #RT window too look in for in source decay products (RT of parent ion plus or minus time_delta)

    with sqlite3.connect(ftrs_filePath) as db:

        sql = "SELECT * FROM Features"

        ff = pd.read_sql(sql, db)
        ff['inferredStructure'] = np.nan
        ff['theo_mwMonoisotopic'] = np.nan
        theo = pd.read_csv(csv_filepath)
        ff.rename(columns={'Id': 'ID', 'apexRetentionTimeMinutes': 'rt', 'apexMwMonoisotopic': 'mwMonoisotopic', 'maxAveragineCorrelation': 'corrMax' }, inplace=True)
        cols_order = ['ID', 'xicStart', 'xicEnd', 'feature', 'corrMax', 'ionCount', 'chargeOrder', 'maxIsotopeCount',
                      'rt', 'mwMonoisotopic','theo_mwMonoisotopic', 'inferredStructure', 'maxIntensity', ]
        ff = ff[cols_order]
        print("Filtering Theo masses by observed masses")
        obs_monomers_df = filtered_theo(ff, theo)
        print("Building multimers from obs muropeptides")
        theo_multimers_df = multimer_builder(obs_monomers_df)
        print("fitering theo multimers by observed")
        obs_multimers_df = filtered_theo(ff,theo_multimers_df)
        print("building custom searh file")
        obs_frames = [obs_monomers_df,obs_multimers_df]
        obs_theo_df = pd.concat(obs_frames).reset_index(drop=True)
        print("generating variants")
        adducts_sodium_df = modification_generator(obs_theo_df,"Sodium")
        adducts_potassium_df = modification_generator(obs_theo_df, "Potassium")
        anhydro_df = modification_generator(obs_theo_df, "Anhydro")
        deacetyl_df = modification_generator(obs_theo_df, "Deacetyl")
        deac_anhy_df = modification_generator(obs_theo_df, "Deacetyl-Anhydro")
        nude_df = modification_generator(obs_theo_df, "Nude")
        decay_df = modification_generator(obs_theo_df, "Decay")

        master_frame = [obs_theo_df,adducts_potassium_df,adducts_sodium_df,anhydro_df,deac_anhy_df,deacetyl_df,decay_df,nude_df]
        master_list = pd.concat(master_frame)
        master_list = master_list.astype({'Monoisotopicmass': float})
        print("Matching")
        matched_data_df = matching(ff,master_list)
        print("Cleaning data")
        cleaned_df = clean_up(matched_data_df,sodium,time_delta_window)
        cleaned_df = clean_up(cleaned_df,potassium,time_delta_window)
        cleaned_data_df = clean_up(cleaned_df,sugar,time_delta_window)

        print("Saving results")
        cleaned_data_df.sort_values('inferredStructure', inplace=True, ascending=True)
        cleaned_data_df.to_csv(ftrs_filePath[:-5] + ' Cleaned' + '.csv', index=False)
        print(ftrs_filePath)
        #Raw matched data for debugging
        # ff.sort_values('inferredStructure', inplace=True, ascending=True)
        # ff.to_csv(ftrs_filePath + 'matched' + '.csv', index=False)

if __name__== "__main__":

    ftrs_filepath = r"C:\Users\ankur\Documents\E coli replicates 2020-07-24\OT_200124_Ecoli_WT_2_Rep1.ftrs"
    csv_filepath = r"C:\Users\ankur\Downloads\Brucella FTRS\E coli disaccharides monomers only.csv"
    main(ftrs_filepath, csv_filepath)