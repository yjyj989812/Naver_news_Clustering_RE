from log import log

@profile
def documents_generator(processed_df: pd.DataFrame, col:str):
    log("Generating documents from dataframe...")
    log("Iteration init")
    for idx, row in processed_df.iterrows():
        if pd.notnull(row[col]):
            yield row[col]  # Yield entire document
        else:
            log(f"null context found in {idx}!", 1)