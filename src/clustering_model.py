from scipy.cluster.hierarchy import linkage
def clustering_model(similarity_matrix):
    # 계층적 병합 클러스터링 
    clustering = linkage(similarity_matrix, method='ward')
    return clustering