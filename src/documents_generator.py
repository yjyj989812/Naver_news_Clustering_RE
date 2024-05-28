import pandas as pd
from line_profiler import profile


@profile
def documents_generator(processed_df: pd.DataFrame, col:str)->pd.Series:
    return processed_df[col].dropna()
    
   
        