import io
import pkgutil

import pandas as pd

def allowed_modifications():
    '''
    Returns allowable modifications stored in a .csv config file. .csv is chosen for consistency of data storage over the project.    
    :return list:
    '''
    data = pkgutil.get_data(__name__, "config/allowed_modifications.csv")    
    allowed_modifications_df  = pd.read_csv(io.BytesIO(data), header=None)
    return allowed_modifications_df[0].tolist()
