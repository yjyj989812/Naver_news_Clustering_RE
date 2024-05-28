from calculate_tfidf import calculate_tfidf
from calculate_cosine_similarity import calculate_cosine_similarity
from clustering_model import clustering_model, reduce_dimensions, retrieve_fcluster
from dendrogram import plot_dendrogram, plot_fcluster
import os, subprocess, json
from urllib import parse
import sqlalchemy
import pandas as pd
import preprocess
from line_profiler import profile
import pathlib
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
BASEDIR = pathlib.Path(__file__).parent.resolve()
with open(os.path.join(BASEDIR.parent, "conn_db.json"), "r", encoding='utf-8') as f:
    keys = json.load(f)

def log(msg, flag=None):    
    if flag==None:
        flag = 0
    head = ["debug", "error", "status"]
    from time import localtime, strftime
    now = strftime("%H:%M:%S", localtime())
    logpath = os.path.join(BASEDIR, "./debug.log")
    if not os.path.isfile(logpath):
        assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" > {logpath}", shell=True)==0, print(f"[error] > shell command failed to execute")
    else: assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" >> {logpath}", shell=True)==0, print(f"[error] > shell command failed to execute")

def retrieve_df(lim:int, table:str)->pd.DataFrame:
    user = keys['user']
    password = keys['password']
    host = keys['host']
    port = keys['port']
    database = keys['database']
    password = parse.quote_plus(password)
    engine = sqlalchemy.create_engine(f"mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    df = pd.read_sql_query("select * from {} LIMIT {}".format(keys[table], lim), con=engine)
    return df

def documents_generator(processed_df: pd.DataFrame, col:str):
    log("Generating documents from dataframe...")
    log("Iteration init")
    for idx, row in processed_df.iterrows():
        if pd.notnull(row[col]):
            yield row[col]  # Yield entire document
        else:
            log(f"null context found in {idx}!", 1)

@profile
def main():
    flag = 0
    try:
        log(f"retrieving dataframe from database...")
        lim = 1000
        log(f"with lim : {lim}")
        df = retrieve_df(lim, "tokenized") # "lake", "tokenized", "warehouse"
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
        datapoints = reduce_dimensions(tfidf_matrix)
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
        z = clustering_model(similarity_matrix)
        clusters = retrieve_fcluster(z, 6, 8)
        
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

    except Exception as e:
        if flag==0: log(f"exception occurred during dataframe retrieval: {e}", 1)
        elif flag==1: log(f"exception occurred during data preprocess: {e}", 1)
        elif flag==2: log(f"exception occurred during tfidf calculation: {e}", 1)
        elif flag==3: log(f"exception occurred during cosine similarity calculation: {e}", 1)
        elif flag==4: log(f"exception occurred during clustering: {e}", 1)
        elif flag==5: log(f"exception occurred during dendrogram plotting: {e}", 1)    
    
if __name__ == "__main__":
    """
        database에서 token화된 news articles를 dataframe으로 retrieve
        -> tf-idf matrix
        -> cosine similarity matrix
        hierarchical agglomerative clustering
    """
    main()