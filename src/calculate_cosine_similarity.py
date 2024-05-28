from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from line_profiler import profile


@profile
def calculate_cosine_similarity(tfidf_matrix):
    """
    tfidf_matrix 'sparse matrix'를 인자로 받아
    코사인 유사도를 리턴

    example:
    문서 갯수: 100건
    similarity_matrix shape: 100 X 100 
    """
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix


# def calculate_cosine_similarity(tfidf_matrix, use_gpu=False):
#     if use_gpu:
#         # GPU를 사용하여 계산하기 위해 TensorFlow GPU 설정
#         physical_devices = tf.config.list_physical_devices('GPU')
#         if physical_devices:
#             tf.config.experimental.set_memory_growth(physical_devices[0], True)
    
#     # 희소 배열을 밀집 배열로 변환
#     tfidf_matrix_dense = tfidf_matrix.toarray()
    
#     # 밀집 배열을 TensorFlow 텐서로 변환
#     tfidf_matrix_tf = tf.constant(tfidf_matrix_dense, dtype=tf.float32)
    
#     # 각 벡터의 L2 norm을 계산
#     norm = tf.norm(tfidf_matrix_tf, axis=1, keepdims=True)
    
#     # 각 벡터를 L2 norm으로 나누어 정규화
#     normalized_matrix = tfidf_matrix_tf / norm
    
#     # 코사인 유사도 계산
#     similarity_matrix = tf.matmul(normalized_matrix, normalized_matrix, transpose_b=True)
    
#     return similarity_matrix.numpy()