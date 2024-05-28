from sklearn.feature_extraction.text import TfidfVectorizer
from line_profiler import profile

@profile
def calculate_tfidf(documents_generator):
    """
    generator 헝식으로 입력 값을 받아 Tf-idf 가중치 계산
    
    
    generator를 통해 생성된 데이터를 'TfidfVectorizer.fit_transform'
    메서드에 전달

    마지막으로 TF-IDF 가중치가 계산된 'tfidf_matrix'를 반환

    input: generator
    output: sparse matrix

    """
    vectorizer = TfidfVectorizer(max_features = 500_000, sublinear_tf = True)
    tfidf_matrix = vectorizer.fit_transform(documents_generator)
    return tfidf_matrix