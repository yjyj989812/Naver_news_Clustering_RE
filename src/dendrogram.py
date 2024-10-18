from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from time import localtime, strftime
import os, pathlib
from line_profiler import profile

CURRENT = pathlib.Path(__file__).parent.resolve()

@profile
def plot_dendrogram(clustering, labels):
    """
    계층적 클러스터링의 덴드로그램을 그리고 저장하는 함수

    Parameters:
        clustering (np.ndarray): 계층적 클러스터링 결과
        labels (List[str]): 라벨이 지정된 배열

    저장된 결과는 'results' 폴더에 저장
    """
    result_path = os.path.join(CURRENT, "results")
    if not os.path.isdir(result_path):
        os.path.mkdir(result_path)

    plt.figure(figsize=(10, 7))
    dendrogram(clustering, labels=labels, orientation='right')
    plt.xlabel('Distance')
    plt.ylabel('Document hash ID')
    plt.title('Hierarchical Clustering Dendrogram')
    now = strftime("%H%M%S", localtime())

    lim = len(labels)
    plt.savefig(os.path.join(CURRENT, f"./results/dendrogram_{now}_size{lim}.png"))
    #plt.show()

@profile
def plot_fcluster(datapoints, clusters, labels):
    """
    클러스터링 결과를 시각화하고 저장하는 함수입니다.

    Parameters:
        datapoints (np.ndarray): 클러스터링 결과로 얻은 데이터 포인트 배열입니다.
        clusters (np.ndarray): 클러스터링 결과로 얻은 클러스터 배열입니다.
        labels (List[str]): 라벨이 지정된 배열입니다.

    저장된 결과는 'results' 폴더에 저장됩니다.
    """
    result_path = os.path.join(CURRENT, "results")
    if not os.path.isdir(result_path):
        os.path.mkdir(result_path)
    plt.figure(figsize=(10, 7))
    plt.scatter(datapoints[:, 0], datapoints[:, 1], c=clusters, cmap='RdYlGn')
    plt.title('Data points and cluster assignments')
    plt.xlabel('PCA-UMAP dim 1')
    plt.ylabel('PCA-UMAP dim 2')
    now = strftime("%H%M%S", localtime())
    lim = len(labels)
    plt.savefig(os.path.join(CURRENT, f"./results/fclusters_{now}_lim{lim}.png"))
    #plt.show()