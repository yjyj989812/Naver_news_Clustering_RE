from calculate_tfidf import calculate_tfidf
from calculate_cosine_similarity import calculate_cosine_similarity
from clustering_model import clustering_model
from dendrogram import plot_dendrogram
import os, subprocess, json
from urllib import parse
import sqlalchemy
import pandas as pd
import preprocess

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
with open(f"conn_db.json", "r", encoding='utf-8') as f:
    keys = json.load(f)

def log(msg, flag=None):    
    if flag==None:
        flag = 0
    head = ["debug", "error", "status"]
    from time import localtime, strftime
    now = strftime("%H:%M:%S", localtime())
    if not os.path.isfile("./debug.log"):
        assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" > debug.log", shell=True)==0, print(f"[error] > shell command failed to execute")
    else: assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" >> debug.log", shell=True)==0, print(f"[error] > shell command failed to execute")

def retrieve_df(lim:int)->pd.DataFrame:
    user = keys['user']
    password = keys['password']
    host = keys['host']
    port = keys['port']
    database = keys['database']
    password = parse.quote_plus(password)
    engine = sqlalchemy.create_engine(f"mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    df = pd.read_sql_query("select * from {} LIMIT {}".format(keys['table'], lim), con=engine)
    return df

def documents_generator(processed_df: pd.DataFrame):
    log("Generating documents from dataframe...")
    log("Iteration init")
    for idx, row in processed_df.iterrows():
        if pd.notnull(row['processed_context']):
            yield row['processed_context']  # Yield entire document
        else:
            log(f"null context found in {idx}!", 1)

def main():
    try:
        log(f"retrieving dataframe from database...")
        lim = 15000
        log(f"with lim : {lim}")
        df = retrieve_df(lim)
    except Exception as e:
        log(f"exception occurred during dataframe retrieval: {e}", 1)
    flag = 0
    try:
        # 전처리
        # null 값 처리
        df = df.dropna()
        log(f"null values removed")
        # 전처리작업을 거친 df를 반환
        log(f"processing on rows...")
        df2 = preprocess.preprocess_df(df=df).copy()
        log("processed columns assigned.")
        # 문서별 정제된 title + context를 기준으로 hash값 생성
        log(f"hash id generating...") 
        df3 = preprocess.create_hash(df2).copy()
        log(f"hash id assigned for each doc.")

        flag += 1 # 1
        # Tf-idf 가중치 계산
        log(f"tfidf calculation init")
        tfidf_matrix = calculate_tfidf(documents_generator(df3))
        log(f"tfidf calculation done")

        flag += 1 # 2
        # 코사인 유사도 계산
        log(f"calculating cosine similarity...")
        similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
        #similarity_matrix = calculate_cosine_similarity(tfidf_matrix, True)
        log(f"cosine similarity calculated")

        flag += 1 # 3
        # 클러스터링 모델
        log(f"clustering init")
        clustering = clustering_model(similarity_matrix)
        log(f"clustering done")

        flag += 1 # 4
        # 덴드로그램 
        # 총 문서 갯수
        num_documents = df.shape[0]
        # 각 문서에 대한 라벨 생성
        document_labels = [f"{df3.iloc[x]['docKey']}" for x in range(num_documents)]
        log(f"plotting init")
        plot_dendrogram(clustering, document_labels)
        log(f"plotting done")

    except Exception as e:
        if flag==0: log(f"exception occurred during data preprocess: {e}", 1)
        elif flag==1: log(f"exception occurred during tfidf calculation: {e}", 1)
        elif flag==2: log(f"exception occurred during cosine similarity calculation: {e}", 1)
        elif flag==3: log(f"exception occurred during clustering: {e}", 1)
        elif flag==4: log(f"exception occurred during dendrogram plotting: {e}", 1)    
    
if __name__ == "__main__":
    """
        database에서 token화된 news articles를 dataframe으로 retrieve
        -> tf-idf matrix
        -> cosine similarity matrix
        hierarchical agglomerative clustering
    """
    main()