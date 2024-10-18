from sklearn.feature_extraction.text import TfidfVectorizer
from line_profiler import profile
import pandas as pd

@profile
def calculate_tfidf(documents:pd.Series):
    """
    documents 데이터를 'TfidfVectorizer.fit_transform'
    메서드에 전달

    TF-IDF 가중치가 계산된 'tfidf_matrix'를 반환

    input: documents
    output: sparse matrix

    """
    vectorizer = TfidfVectorizer(max_features = 500_000, sublinear_tf = True)
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix