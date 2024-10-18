# 네이버 뉴스 클러스터링 알고리즘 역공학 및 의미 분석


## 프로젝트 개요
본 프로젝트는 네이버 뉴스 서비스에서 사용 중인 [뉴스 클러스터링 알고리즘](https://media.naver.com/algorithm)을 역공학한 후, 이를 Kagge 영어 뉴스 도메인에 적용하여 기사 분류를 시행합니다. 최종적으로 각 클러스터 별로 LDA 및 TF-IDF 의미 분석을 시행하여 각 클러스터 별로 어떤 의미를 담고 있는지를 그리고 어떤 기준으로 군집을 생성하였는지를 살펴봅니다.


## Dataset
본 프로젝트의 데이터셋은 Kaggle 영어 뉵스 데이터셋을 사용하였으며, 기사 본문, 기사 제목, 작성일과 출처가 포함되여 있습니다.

- **Source:** [Kaggle News Articles Dataset](https://www.kaggle.com/snapcrack/all-the-news)
- **Attributes Used:** Article text
- **Source:** [Kaggle News Articles Dataset](https://www.kaggle.com/snapcrack/all-the-news)
- **Attributes Used:** Article text
- **Source:** [Kaggle News Articles Dataset](https://www.kaggle.com/snapcrack/all-the-news)
- **Attributes Used:** Article text


## 사용한 방법론(Methodology)
1. **Data Preprocessing:** 
    - Text cleaning (removing stopwords, punctuation, etc.)
    - Tokenization
2. **TF-IDF Vectorization:** 
    - Convert text data to TF-IDF vectors
3. **Hierarchical Clustering:** 
    - Perform hierarchical clustering on TF-IDF vectors
4. **LDA Topic Modeling:** 
    - Apply LDA to each cluster to extract topics


## 설치
To run this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/news-clustering-lda.git
    cd news-clustering-lda
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```


## 방법론 별 적용법
1. **Preprocess the Data:**
    ```bash
    python preprocess.py
    ```
2. **Vectorize using TF-IDF:**
    ```bash
    python vectorize.py
    ```
3. **Perform Hierarchical Clustering:**
    ```bash
    python cluster.py
    ```
4. **Topic Modeling with LDA:**
    ```bash
    python lda.py
    ```
5. **Visualize Results:**
    ```bash
    python visualize.py
    ```


## 결과
The project outputs include:
- Dendrogram of the hierarchical clustering
- Clusters of news articles
- Topics identified within each cluster using LDA
- Visualizations of the topics and clusters


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
