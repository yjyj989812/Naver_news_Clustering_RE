import pandas as pd
import numpy as np
import clustering_model
from log import log
def retrieve_cluster_results(df:pd.DataFrame, clusters):
    result_df = df.copy()
    docs_cluster_numberings = {}
    num_clusters = len(np.unique(clusters))
    for clust_idx in range(1, num_clusters+1):
        for docKey in clustering_model.get_cluster_documents(df, clusters, clust_idx):
            docs_cluster_numberings[docKey] = clust_idx
    result_df['cluster_num'] = result_df['docKey'].apply(lambda x: docs_cluster_numberings[x])
    return result_df