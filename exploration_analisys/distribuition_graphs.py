import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

def generate_dist_plots(data: pd.DataFrame):
    all_graphs = []
    types = ['int8','int16','int32','int64','int128','float8','float16','float32','float64','float128']
    for col in data.columns:
        if (data[col].dtype in types):
            figure = px.histogram(data, x=col,
                        width=600, height=600, 
                    title=f"Histogram of variable {col}")
            figure.update_layout(
                yaxis_title="Occurrences"
            )
            
            
            
            all_graphs.append(figure)
            #figure.show()
    
    return all_graphs