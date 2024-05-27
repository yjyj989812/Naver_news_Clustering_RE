# import packages
from num2words import num2words
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from sqlalchemy import text
import urllib.parse
import json
import tqdm
import pandas as pd
from babel.numbers import get_currency_name
import cityhash
# data processing 
class text_processor:
    def __init__(self, text):
        self.text = f"""{text.lower()}"""
        
    def replace_percent(self):
        self.text= re.sub(r'%', ' percent', self.text)
        return self
    
    def replace_currency_symbols(self):
        replacements = {
            '$': get_currency_name(' USD', locale='en'),
            '£': get_currency_name(' GBP', locale='en'),
            '€': get_currency_name(' EUR', locale='en'),
            '¥': get_currency_name(' JPY', locale='en'),
            '₩': get_currency_name(' KRW', locale='en')
        }
        for symbol, name in replacements.items():
            self.text = self.text.replace(symbol, name)
        return self
    
    def split_unit(self):
        def replacer(match):
            if match.group(1) and match.group(2):
                # number+alph
                return f"{match.group(1)} {match.group(2)}"
            elif match.group(3) and match.group(4):
                # alph+number
                return f"{match.group(3)} {match.group(4)}"
            return match.group(0)
        
    def number_to_word(self):
        self.text = re.sub(r'\d+', lambda x: num2words(int(x.group())), self.text)
        return self
    
    def remove_tab_enter(self):
        self.text = re.sub(r'\t|\n', ' ', self.text)
        return self
    
    def delete_special(self):
        pattern = r'[^a-zA-Z0-9\s]'
        self.text = re.sub(pattern, ' ', self.text) 
        return self
    
    def process_all(self):
        if '%' in self.text:
            self.replace_percent()
        elif '$£€¥₩' in self.text:
            self.replace_currency_symbols()
        elif '\n' in self.text or '\t' in self.text:
            self.remove_tab_enter()
        self.split_unit()
        self.number_to_word()
        self.delete_special()
        return self.text


# 영어 뉴스 전체  dataFrame에서 null값이 있는 case 제외한 나머지를 df로 반환
def remove_null_rows(df):
    return df[~df.isna().any(axis=1)]

# text_processor를 통해 전처리작업을 거친 df를 반환
def preprocess_df(df):
    df['processed_title'] = df['title'].apply(lambda x: text_processor(x).process_all() if pd.notnull(x) else x)
    df['processed_context'] = df['context'].apply(lambda x: text_processor(x).process_all() if pd.notnull(x) else x)
    return df

# 영어 뉴스 dataFrame에서 title과 context를 합친 값을 입력으로 cityhash 함수를 사용해 각 요소의 hash key을 생성함
# 생성한 hash key는 'docKey'의 column으로 저장됨
def create_hash(df):
    df.loc[:,'docKey'] = pd.DataFrame(df.loc[:,'processed_title'] + df.loc[:,'processed_context']).map(lambda x: str(cityhash.CityHash64(x)))
    return df