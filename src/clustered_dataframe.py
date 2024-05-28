from clustering_model import get_cluster_documents
import numpy as np
import pandas as pd
from line_profiler import profile

@profile
def retrieve_cluster_results(df:pd.DataFrame, clusters):
    result_df = df.copy()
    docs_cluster_numberings = {}
    num_clusters = len(np.unique(clusters))


    for clust_idx in range(1, num_clusters+1):
        for docKey in get_cluster_documents(df, clusters, clust_idx):
            docs_cluster_numberings[docKey] = clust_idx
    result_df['cluster_num'] = result_df['docKey'].map(docs_cluster_numberings)
    
    
    print(result_df)
    
    return result_df