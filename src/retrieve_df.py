import pandas as pd
from urllib import parse
import sqlalchemy
import json

def retrieve_df(lim:int, table:str, keys:json)->pd.DataFrame:
    """
    데이터베이스 연동 및 table 데이터 추출
    """
    user = keys.get('user')
    password = keys.get('password')
    host = keys.get('host')
    port = keys.get('port')
    database = keys.get('database')
    table = keys.get('table')
    password = parse.quote_plus(password)
    engine = sqlalchemy.create_engine(f"mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    df = pd.read_sql_query("select * from {} LIMIT {}".format(table, lim), con=engine)
    return df