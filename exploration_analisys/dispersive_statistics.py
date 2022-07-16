import pandas as pd
import numpy as np

def generate_dispersive_statistics(data: pd.DataFrame):
    types = ['int8','int16','int32','int64','int128','float8','float16','float32','float64','float128']
    data_temp = data.copy()
    for col in data_temp.columns:
        if (data_temp[col].dtype not in types):
            data_temp = data_temp.drop(col)
    
    dict_metrics = {}
    metrics = ['mean','median','std','q1','q2','q3','var']
    for col in data_temp.columns:
        dict_aux = {}
        for metric in metrics:
            if (metric == 'mean'):
                dict_aux['mean'] = data_temp[col].mean()
            elif (metric == 'median'):
                dict_aux['median'] = data_temp[col].median()
            elif (metric == 'std'):
                dict_aux['std'] = data_temp[col].std()
            elif (metric == 'q1'):
                dict_aux['q1'] = data_temp[col].quantile(0.25)
            elif (metric == 'q2'):
                dict_aux['q2'] = data_temp[col].quantile(0.50)
            elif (metric == 'q3'):
                dict_aux['q3'] = data_temp[col].quantile(0.75)
            else:
                dict_aux['var'] = data_temp[col].var()
        dict_metrics[col] = dict_aux


    return dict_metrics
    
