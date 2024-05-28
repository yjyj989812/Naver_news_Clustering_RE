from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from time import localtime, strftime
import os, pathlib

CURRENT = pathlib.Path(__file__).parent.resolve()

def plot_dendrogram(clustering, labels):
    plt.figure(figsize=(10, 7))
    dendrogram(clustering, labels=labels, orientation='right')
    plt.xlabel('Distance')
    plt.ylabel('Document hash ID')
    plt.title('Hierarchical Clustering Dendrogram')
    now = strftime("%H_%M_%S", localtime())
    lim = len(labels)
    plt.savefig(os.path.join(CURRENT, f"./results/dendrogram_{now}_lim{lim}.png"))
    plt.show()
    
def plot_fcluster(datapoints, clusters, labels):
    # 각 클러스터별 데이터 포인트 시각화
    plt.figure(figsize=(10, 7))
    plt.scatter(datapoints[:, 0], datapoints[:, 1], c=clusters, cmap='prism')
    plt.title('Data points and cluster assignments')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    now = strftime("%H_%M_%S", localtime())
    lim = len(labels)
    plt.savefig(os.path.join(CURRENT, f"./results/fclusters_{now}_lim{lim}.png"))
    plt.show()