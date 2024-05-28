from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

def plot_dendrogram(clustering, labels):
    plt.figure(figsize=(10, 7))
    dendrogram(clustering, labels=labels, orientation='right')
    plt.xlabel('Distance')
    plt.ylabel('Document hash ID')
    plt.title('Hierarchical Clustering Dendrogram')
    plt.savefig("./dendrogram.png")
    plt.show()