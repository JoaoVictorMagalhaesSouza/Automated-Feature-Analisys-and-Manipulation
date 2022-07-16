import pandas as pd
import numpy as np

def generate_dispersive_statistics(data: pd.DataFrame):
    types = ['int8','int16','int32','int64','int128','float8','float16','float32','float64','float128']
    data_temp = data.copy()
    for col in data_temp.columns:
        if (data_temp[col].dtype not in types):
            data_temp = data_temp.drop(col)
    
    df_statistics = data_temp.describe()
    return df_statistics
    
