# custom packages
from calculate_tfidf import calculate_tfidf
from calculate_cosine_similarity import calculate_cosine_similarity
import clustering_model
from retrieve_df import retrieve_df
from dendrogram import plot_dendrogram, plot_fcluster
from log import log
from documents_generator import documents_generator
# external packages
import os, pathlib, json
import numpy as np


BASEDIR = pathlib.Path(__file__).parent.resolve()


with open(os.path.join(BASEDIR.parent, "conn_db.json"), "r", encoding='utf-8') as f:
    keys = json.load(f)


@profile
def main():
    flag = 0
    try:
        log(f"retrieving dataframe from database...")
        lim = 10000
        log(f"with lim : {lim}")
        df = retrieve_df(lim, "tokenized", keys) # "lake", "tokenized", "warehouse"
        flag += 1 # 1
        # 전처리
        # null 값 처리
        # df = df.dropna()
        # log(f"null values removed")
        # # 전처리작업을 거친 df를 반환
        # log(f"processing on rows...")
        # df2 = preprocess.preprocess_df(df=df).copy()
        # log("processed columns assigned.")
        # # 문서별 정제된 title + context를 기준으로 hash값 생성
        # log(f"hash id generating...") 
        # df3 = preprocess.create_hash(df2).copy()
        # log(f"hash id assigned for each doc.")

        flag += 1 # 2
        # Tf-idf 가중치 계산
        log(f"tfidf calculation init")
        tfidf_matrix = calculate_tfidf(documents_generator(df, "tokens"))
        datapoints = clustering_model.reduce_dimensions(tfidf_matrix)
        log(f"tfidf calculation done")

        flag += 1 # 3
        # 코사인 유사도 계산
        log(f"calculating cosine similarity...")
        similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
        #similarity_matrix = calculate_cosine_similarity(tfidf_matrix, True)
        log(f"cosine similarity calculated")

        flag += 1 # 4
        # 클러스터링 모델
        log(f"clustering init")
        z = clustering_model.clustering_model(similarity_matrix)
        min_clusters = 4
        max_clusters = 8
        clusters = clustering_model.retrieve_fcluster(z, min_clusters, max_clusters)
        
        log(f"clustering done")

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
        num_clusters = len(np.unique(clusters))
        for clust_idx in range(1, num_clusters+1):
            cluster_docs = clustering_model.get_cluster_documents(df, clusters, clust_idx)
            log(f"size of cluster #{clust_idx} = {len(cluster_docs)}")

    except Exception as e:
        if flag==0: log(f"exception occurred during dataframe retrieval: {e}", 1)
        elif flag==1: log(f"exception occurred during data preprocess: {e}", 1)
        elif flag==2: log(f"exception occurred during tfidf calculation: {e}", 1)
        elif flag==3: log(f"exception occurred during cosine similarity calculation: {e}", 1)
        elif flag==4: log(f"exception occurred during clustering: {e}", 1)
        elif flag==5: log(f"exception occurred during dendrogram plotting: {e}", 1)
        elif flag==6: log(f"exception occurred during cluster result analysis: {e}", 1)
    
if __name__ == "__main__":
    """
        database에서 token화된 news articles를 dataframe으로 retrieve
        -> tf-idf matrix
        -> cosine similarity matrix
        hierarchical agglomerative clustering
    """

    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    

    main()