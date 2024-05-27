from calculate_tfidf import calculate_tfidf
from calculate_cosine_similarity import calculate_cosine_similarity
from clustering_model import clustering_model
from dendrogram import plot_dendrogram


def main(file_path):
    # 총 문서 갯수
    num_documents = 0

    # 각 문서에 대한 라벨 생성
    document_labels = [f"Document{x}" for x in range(1, num_documents+1)]
    



    # Tf-idf 가중치 계산
    # documents_generator 필요
    # tfidf_matrix = calculate_tfidf(documents_generator)
    
    # 코사인 유사도 계산
    # similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
    
    # 클러스터링 모델
    # clustering = clustering_model(similarity_matrix)

    # 덴드로그램 
    #plot_dendrogram(clustering, document_labels)






if __name__ == "__main__":
    file_path = ""
    """
    git merge
    """
    main(file_path)