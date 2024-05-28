from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from time import localtime, strftime
import os, pathlib

CURRENT = pathlib.Path(__file__).parent.resolve()

@profile
def plot_dendrogram(clustering, labels):
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
    plt.savefig(os.path.join(CURRENT, f"./results/dendrogram_{now}_lim{lim}.png"))
    #plt.show()

@profile
def plot_fcluster(datapoints, clusters, labels):
    # 각 클러스터별 데이터 포인트 시각화
    result_path = os.path.join(CURRENT, "results")
    if not os.path.isdir(result_path):
        os.path.mkdir(result_path)
    plt.figure(figsize=(10, 7))
    plt.scatter(datapoints[:, 0], datapoints[:, 1], c=clusters, cmap='prism')
    plt.title('Data points and cluster assignments')
    plt.xlabel('t-SNE dim 1')
    plt.ylabel('t-SNE dim 2')
    now = strftime("%H%M%S", localtime())
    lim = len(labels)
    plt.savefig(os.path.join(CURRENT, f"./results/fclusters_{now}_lim{lim}.png"))
    #plt.show()