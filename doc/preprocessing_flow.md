# Preprocessing Flow
## 작성일: 2024-05-27
## 개요: Newsdata 전처리 과정 확정을 위한 회의 결론

- - -

## 흐름도
### 1. DB lake에서 데이터 가져오기   
- DB table: english_news_lake

dataSource | title | context |

### 2. 들고온 dataset 전처리
#### 2-1. Null값 제거
- 제거 함수는 `preprocessing_fun.py`에 있음

#### 2-2. 숫자,영어 또는 영어,숫자 붙어있는 것 띄우기
- `processing.ipynb` 파일에 있음

#### 2-3. \n, \t 제거 (escape 문자)
- `processing.ipynb` 파일에 있음

#### 2-4. 숫자 제거
- 추가 필요

#### 2-5. 통화 기호(달러, 유로, 등) 단어로 변환
- `processing.ipynb` 파일에 있음

#### 2-6. 특수기호 제거
- 추가 필요

#### 2-7. hash key 생성
- 생성함수는 `preprocessing_fun.py`에 있음

#### 2-8. hash 포함, 전처리된 df를 DB에 전송
- 추가 필요 (담당: 유정연)
- Table 명: english_news_warehouse   

| dataSource | title | context | docKey |

- - -
### 3. Tokenizer
#### tokenizer로 token화
#### 어간 추출

- - -

#### TF-IDF로 백터화
#### 코사인 유사도
#### 코사인 유사도 기반 Clustering