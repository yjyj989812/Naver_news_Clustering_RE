import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV, StratifiedKFold, LeaveOneOut, ShuffleSplit


def remove_meaningless_tokens(df: pd.DataFrame, col_name='tokens', token_len=3):
    df[col_name] = df.loc[:, col_name].map(lambda x: ' '.join([token for token in x.split() if len(token) > token_len]))
    return df


def get_tfidf_for_lda(documents_generator):
    """
    generator 헝식으로 입력 값을 받아 Tf-idf 가중치 계산
    generator를 통해 생성된 데이터를 'TfidfVectorizer.fit_transform' 메서드에 전달
    마지막으로 TF-IDF 가중치가 계산된 'tfidf_matrix'를 반환 및 LDA에 필요한 요소 반환

    input: generator
    output: sparse matrix, tf-idf vocabulary, vocabulary feature outs, transformed vectorizer
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents_generator)
    vocabulary = vectorizer.vocabulary_
    voca_feature_names = vectorizer.get_feature_names_out()
    return tfidf_matrix, vocabulary, voca_feature_names, vectorizer


def get_top_tfidf_words(tfidf_matrix, vocabulary, top_n=10):
    # TF-IDF 행렬을 배열 형태로 변환
    tfidf_array = tfidf_matrix.toarray()
    
    # 각 단어의 TF-IDF 값과 단어를 추출
    words_tfidf = []
    for i, word in enumerate(vocabulary):
        tfidf_value = tfidf_array[:, i].sum()  # 모든 문서에 대해 단어의 TF-IDF 값을 합산
        words_tfidf.append((word, tfidf_value))
    
    # TF-IDF 값에 따라 단어를 정렬 (내림차순)
    sorted_words_tfidf = sorted(words_tfidf, key=lambda x: x[1], reverse=True)
    
    # 상위 top_n개의 단어와 TF-IDF 값을 반환
    return sorted_words_tfidf[:top_n]


def record_tfidf_top_words_by_cluster(top_tfidf_words, cluster_name=0):
    result = {}
    for word, score in top_tfidf_words:
        result[word] = score

    with open(f'cluster_{cluster_name}_top_words.json', 'w') as f:
        json.dump(result, f)


def search_lda_parameters_grid(tfidf_matrix):
    lda_model = LatentDirichletAllocation(
    learning_method='online',
    random_state=42,
    )

    # GridSearchCV를 위한 하이퍼파라미터 그리드 설정
    param_grid = {
        'n_components': [3, 4, 5, 6, 7, 8, 9 ,10],  # 토픽 수
        'learning_decay': [0.5, 0.7, 0.9],  # 온라인 학습의 학습 감쇠율
        'doc_topic_prior': [0.1, 0.5, 1],  # α
        'topic_word_prior': [0.1, 0.5, 1]  # β
    }

    # cv options
    # skf = StratifiedKFold(n_splits=5) # n_splits = 3, 5, 10
    # LeaveOneOut()
    sfs = ShuffleSplit(n_splits=10, test_size=0.2, random_state=42)

    # GridSearchCV 설정
    grid_search = GridSearchCV(lda_model, param_grid, cv=3, n_jobs=-1, verbose=2)

    # GridSearchCV 실행
    grid_search.fit(tfidf_matrix)
    return grid_search.best_params_


def train_lda_with_optimal(best_params, tfidf_matrix, max_iter_=10):
    # 최적의 하이퍼파라미터로 LDA 모델 학습
    optimal_lda = LatentDirichletAllocation(
        n_components=best_params['n_components'],
        learning_method='online',
        learning_decay=best_params['learning_decay'],
        doc_topic_prior=best_params['doc_topic_prior'],
        topic_word_prior=best_params['topic_word_prior'],
        random_state=42,
        max_iter=max_iter_
    )

    optimal_lda.fit(tfidf_matrix)
    return optimal_lda


def print_top_topics(components, feature_names, token_n=5):
    for idx, topic in enumerate(components):
        print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-token_n - 1:-1]])


def record_top_topics_by_cluster(components, feature_names, token_n=5, label_name=0):
    topic_result = {}
    for idx, topic in enumerate(components):
        topic_result[f'Topic {idx+1}'] = [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-token_n - 1:-1]]

    with open(f'cluster_{label_name}_topic_result.json', 'w') as f:
        json.dump(topic_result, f)