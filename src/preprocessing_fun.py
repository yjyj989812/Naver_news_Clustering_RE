import pandas as pd
import cityhash

# dataset load from DB
# sample_df = pd.read_sql_query(sql='SELECT * FROM english_news_lake;', con=engine)


# 영어 뉴스 전체  dataFrame에서 null값이 있는 case 제외한 나머지를 df로 반환
def remove_null_rows(total_df):
    return total_df[~total_df.isna().any(axis=1)]


# 영어 뉴스 dataFrame에서 title과 context를 합친 값을 입력으로 cityhash 함수를 사용해 각 요소의 hash key을 생성함
# 생성한 hash key는 'docKey'의 column으로 저장됨
def create_hash(total_df):
    total_df.loc[:,'docKey'] = pd.DataFrame(total_df.loc[:,'title'] + total_df.loc[:,'context']).map(lambda x: str(cityhash.CityHash64(x)))

    return total_df