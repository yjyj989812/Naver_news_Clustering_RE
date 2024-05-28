from clustering_model import get_cluster_documents
import numpy as np
import pandas as pd
from line_profiler import profile


@profile
def retrieve_cluster_results(df:pd.DataFrame, clusters):
    """
    클러스터링 결과를 기반으로 각 문서에 클러스터 번호를 매핑하여 새로운 열로 추가하는 함수

    Parameters:
        df (pd.DataFrame): 문서 데이터프레임
        clusters (np.ndarray): 각 문서에 할당된 클러스터 번호가 포함된 배열

    Returns:
        pd.DataFrame: 클러스터 번호가 추가된 새로운 데이터프레임

    클러스터링 결과를 바탕으로 각 문서에 할당된 클러스터 번호를 계산하고, 이를 새로운 열로 추가하여 반환
    """
    result_df = df.copy()
    docs_cluster_numberings = {}
    num_clusters = len(np.unique(clusters))

    for clust_idx in range(1, num_clusters+1):
        for docKey in get_cluster_documents(df, clusters, clust_idx):
            docs_cluster_numberings[docKey] = clust_idx
    result_df['cluster_num'] = result_df['docKey'].map(docs_cluster_numberings)

    return result_df

@profile
def dataframe_rand_selection(df:pd.DataFrame, num_rows:int=None):
    """
    데이터프레임에서 절반의 행을 랜덤하게 선택하여 새로운 데이터프레임을 반환하는 함수

    Parameters:
        df (pd.DataFrame): 원본 데이터프레임
    Returns:
        new_df (pd.DataFrame): 랜덤하게 선택된 행으로 이루어진 새로운 데이터프레임
        labels (list): 선택된 행들의 hash 값들의 list

    데이터프레임에서 절반의 행을 랜덤하게 선택하여 새로운 데이터프레임과 선택된 행들의 hash id를 반환
    """
    np.random.seed(42)
    if num_rows == None:
        num_rows = df.shape[0]
        num_rows = num_rows // 2
    selected_rows = np.random.choice(df.index, num_rows)
    new_df = df.loc[selected_rows]
    #labels = df.iloc[selected_rows, 0].tolist()
    return new_df