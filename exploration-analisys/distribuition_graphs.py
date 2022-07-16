import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

def generate_dist_plots(data: pd.DataFrame):
    all_graphs = []
    for col in data.columns:
        figure = px.histogram(data, x=col,
                    width=600, height=600, 
                   title=f"Distribuition graph of variable {col}")
        
        
        
        all_graphs.append(figure)
        #figure.show()
    
    return all_graphs