import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from num2words import num2words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import re
from typing import List, Generator
import csv
import pandas as pd

@profile
def generate_doc(file_path, text_column):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            yield row[text_column]

@profile
def preprocessing(documents):
    stop_words = set(stopwords.words("english"))
    wordnet_lemmatizer = WordNetLemmatizer()
    
    for text in documents:
        text = str(text).lower()
        tokens = word_tokenize(text)
        tokens = [i.replace(",", "") for i in tokens]
        tokens = [num2words(i) if i.isdigit() else i for i in tokens]
        adj_text = " ".join(tokens)
        adj_text = re.sub(r'^[^a-z]', ' ', adj_text)
        tokens = word_tokenize(adj_text)
        tokensWSW = [word for word in tokens if word not in stop_words]
        lemmatized_list = [wordnet_lemmatizer.lemmatize(word) for word in tokensWSW]
        clean_text = " ".join(lemmatized_list)
        yield clean_text

@profile
def calculate_tfidf(documents_generator):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents_generator)
    return tfidf_matrix

@profile
def calculate_cosine_similarity(tfidf_matrix):
    # 코사인 유사도 계산
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

@profile
def clustering_model(similarity_matrix):
    # 계층적 병합 클러스터링 수행
    clustering = linkage(similarity_matrix, method='ward')
    return clustering

@profile
def plot_dendrogram(clustering, labels):
    plt.figure(figsize=(10, 7))
    dendrogram(clustering, labels=labels, orientation='right')
    plt.xlabel('Distance')
    plt.ylabel('Document')
    plt.title('Hierarchical Clustering Dendrogram')
    plt.show()

@profile
def main(file_path):
    file_path = "aticle_sample.csv"
    text_column = "context"

    num_documents = sum(1 for _ in generate_doc(file_path, text_column))

    document_labels = ['Document{}'.format(i) for i in range(1, num_documents + 1)]

    documents_generator = generate_doc(file_path, text_column)
    preprocessing_documents =  preprocessing(documents_generator)
    tfidf_matrix = calculate_tfidf(preprocessing_documents)
    similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
    clustering = clustering_model(similarity_matrix)
    plot_dendrogram(clustering, labels = document_labels)

if __name__ == "__main__":
    file_path = ""
    main(file_path)
    