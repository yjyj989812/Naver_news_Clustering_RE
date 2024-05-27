from sklearn.metrics.pairwise import cosine_similarity
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
