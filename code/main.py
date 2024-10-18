import os, subprocess, json
from urllib import parse
import sqlalchemy
import nltk
import pandas as pd
import preprocess


with open(f"..\\conn_db.json", "r", encoding='utf-8') as f:
    keys = json.load(f)


def log(msg, flag=None):
    if flag==None:
        flag = 0
    head = ["debug", "error", "status"]
    from time import gmtime, strftime
    now = strftime("%H:%M:%S", gmtime())
    if not os.path.isfile("./debug.log"):
        assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" > debug.log", shell=True)==0, print(f"[error] > shell command failed to execute")
    else: assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" >> debug.log", shell=True)==0, print(f"[error] > shell command failed to execute")


def retrieve_df():
    engine = establish_conn()
    return pd.read_sql_query("select * from english_news_lake", con=engine)


def establish_conn()->sqlalchemy.Engine:
    user = keys['user']
    password = keys['password']
    host = keys['host']
    port = keys['port']
    database = keys['database']
    password = parse.quote_plus(password)
    engine = sqlalchemy.create_engine(f"mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    return engine


def documents_generator(df:pd.DataFrame):
    log(f"generating documents from dataframe...")
    log(f"iteration init")
    for idx, row in df.iterrows():
        log(f"iteration index : {idx}, row : {row}")
        yield from row['processed_context']


def main():
    log(f"retrieving dataframe from database...")
    df = retrieve_df()
    # 총 문서 갯수
    num_documents = df.shape[0]
    # 각 문서에 대한 라벨 생성
    document_labels = [f"Document{x}" for x in range(1, num_documents+1)]

    # 전처리
    # null 값 처리
    df = preprocess.remove_null_rows(df=df).copy()
    log(f"df shape={df.shape}")
    log(f"null values removed")
    # 전처리작업을 거친 df를 반환
    log(f"processing on rows...")
    df2 = preprocess.preprocess_df(df=df).copy()
    log(f"df2 shape={df2.shape}")
    log("processed columns assigned.")
    # 문서별 정제된 title + context를 기준으로 hash값 생성
    log(f"hash id generating...") 
    df3 = preprocess.create_hash(df2).copy()
    log(f"df3 shape={df3.columns.tolist()}")
    log(f"hash id assigned for each doc.")

    
if __name__ == "__main__":
    # download from nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    """
    변경사항
    """
    main()