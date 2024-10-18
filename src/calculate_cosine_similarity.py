from sklearn.metrics.pairwise import cosine_similarity
from line_profiler import profile
import cupy as cp
import cupyx.scipy.sparse

@profile
def calculate_cosine_similarity(tfidf_matrix):
    """
    tfidf_matrix 'sparse matrix'를 인자로 받아
    코사인 유사도를 리턴

    example:
    문서 갯수: 100건
    similarity_matrix shape: 100 X 100 
    """
    similarity_matrix = cosine_similarity(tfidf_matrix, dense_output=False)
    
    return similarity_matrix

@profile
def calculate_cosine_similarity_gpu(tfidf_matrix):
    """
    tfidf_matrix 'sparse matrix'를 인자로 받아
    코사인 유사도를 리턴

    Parameters:
    tfidf_matrix (scipy.sparse.csr_matrix): TF-IDF 행렬.

    Returns:
    cupy.ndarray: 코사인 유사도 행렬.
    """
    # 희소 행렬을 Cupy로 변환
    tfidf_matrix_gpu = cp.sparse.csr_matrix(tfidf_matrix)

    # 각 행의 L2 노름을 계산
    norm = cp.sqrt((tfidf_matrix_gpu.multiply(tfidf_matrix_gpu)).sum(axis=1))

    # 코사인 유사도 계산
    similarity_matrix = tfidf_matrix_gpu.dot(tfidf_matrix_gpu.T) / (norm.dot(norm.T) + 1e-10)

    return similarity_matrix