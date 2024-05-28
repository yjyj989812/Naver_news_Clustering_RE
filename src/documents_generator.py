from log import log
import pandas as pd
from line_profiler import profile


@profile
def documents_generator(processed_df: pd.DataFrame, col:str):
    log("Generating documents from dataframe...")
    log("Iteration init")
    return processed_df[col].dropna()
    
    # for idx, row in processed_df.iterrows():
    #     if pd.notnull(row[col]):
    #         yield row[col]  # Yield entire document
        