# custom packages
from calculate_tfidf import calculate_tfidf
from calculate_cosine_similarity import calculate_cosine_similarity
from dendrogram import plot_dendrogram, plot_fcluster
from retrieve_df import retrieve_df
from documents_generator import documents_generator
from clustered_dataframe import retrieve_cluster_results, dataframe_rand_selection
from clustering_model import clustering_model, reduce_dimensions, get_cluster_documents, retrieve_fcluster
from log import log, logging

# external packages
import os, json, pickle, pathlib
import numpy as np
from line_profiler import profile

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
BASEDIR = pathlib.Path(__file__).parent.resolve()
with open(os.path.join(BASEDIR, "../conn_db.json"), "r", encoding='utf-8') as f:
    keys = json.load(f)

@profile
def main():
    flag = 0
    try:
        # DB에서 Dataframe 추출
        log(f"retrieving dataframe from database...")
        lim = 1000
        log(f"with lim : {lim}")
        df = retrieve_df(lim, "tokenized", keys) # "lake", "tokenized", "warehouse"
        
        flag += 1 # 1
        # Dataframe에서 랜덤하게 절반의 크기로 선택
        log(f"random selection on progress...")
        filtered_df, label_index = dataframe_rand_selection(df)
        # random으로 선택된 row들이기 때문에 index를 초기화
        df = filtered_df.reset_index(drop=True)
        log(f"random selection done with shape of {df.shape}")
        col = "tokens"
        log("Generating documents from dataframe...")
        documents = documents_generator(df, col)
        log(f"document generation done.")


        flag += 1 # 2
        # Tf-idf 가중치 계산
        log(f"tfidf calculation init")
        tfidf_matrix = calculate_tfidf(documents)
        log(f"tfidf calculation done")

        # PCA와 t-SNE를 통한 차원 축소 및 데이터포인트 생성
        datapoints = reduce_dimensions(tfidf_matrix)
        log(f"dimension reduction done.")
        

        flag += 1 # 3
        # 코사인 유사도 계산
        log(f"calculating cosine similarity...")
        similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
        #similarity_matrix = calculate_cosine_similarity(tfidf_matrix, True)
        log(f"cosine similarity calculated")


        flag += 1 # 4
        # 클러스터링 모델
        log(f"clustering init")
        z = clustering_model(similarity_matrix.toarray())
        log(f"linkage done.")
        min_clusters = 4
        max_clusters = 8
        # silhouette scoring을 통해 최적의 클러스터 개수를 탐색
        log(f"scoring clustering result with size between minimum {min_clusters} and maximum {max_clusters}")
        clusters, num_clusters = retrieve_fcluster(z, min_clusters, max_clusters, datapoints)
        log(f"clustering done with best cluster number of {num_clusters}")

        flag += 1 # 5
        # 덴드로그램 
        # 총 문서 갯수
        num_documents = df.shape[0]
        # 각 문서에 대한 라벨 생성
        document_labels = [f"{df.iloc[x]['docKey']}" for x in range(num_documents)]
        log(f"plotting init")
        plot_dendrogram(z, document_labels)
        plot_fcluster(datapoints, clusters, document_labels)
        log(f"plotting done")
        
        flag += 1 # 6
        with open(os.path.join(BASEDIR, "./results/result_df.pkl"), "wb") as f:
            pickle.dump(retrieve_cluster_results(df, clusters), f)
        for clust_idx in range(1, num_clusters+1):
            cluster_docs = get_cluster_documents(df, clusters, clust_idx)
            log(f"size of cluster #{clust_idx} = {len(cluster_docs)}")


    except Exception as e:
        logging(flag, e)
    
if __name__ == "__main__":
    """
        database에서 token화된 news articles를 dataframe으로 retrieve
        -> tf-idf matrix
        -> cosine similarity matrix
        hierarchical agglomerative clustering
    """


    main()