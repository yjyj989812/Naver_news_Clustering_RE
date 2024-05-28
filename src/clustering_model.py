import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

def clustering_model(similarity_matrix):
    # 코사인 유사도 행렬의 대각선을 1로 채워줌.
    np.fill_diagonal(similarity_matrix, 1)

    # 거리 행렬로 변환
    distance_matrix = 1 - similarity_matrix
    
    # 거리 행렬을 대칭 행렬로 만들기 위해 아래와 같이 대칭행렬로 변환
    distance_matrix_symmetric = (distance_matrix + distance_matrix.T) / 2
    
    # 음수 값을 0으로 만들어줌
    distance_matrix_symmetric[distance_matrix_symmetric < 0] = 0
    
    # 행렬로 변환
    condensed_distance = squareform(distance_matrix_symmetric)
    
    # 계층적 병합 클러스터링 
    z = linkage(condensed_distance, method='ward')
    return z