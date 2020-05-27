import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from sys import exit
import seaborn as sns

from graph import *
from utils import Timer


def draw_scale_free():
    timer = Timer()
    graph = ScaleFree(1000, 2)
    print(f'Elapsed for generation {timer.measure()}')
    print(f'Average degree = {graph.average_degree()}')
    degs = graph.degrees()
    x = [np.log(d) for d in degs.keys()]
    y = [np.log(c) for c in degs.values()]
    plt.scatter(x, y)
    plt.show()


def draw_small_world(n, k, beta):
    timer = Timer()
    graph = SmallWorld(n, k, beta)
    print(f'Elapsed for generation {timer.measure()}')
    print(f'Average degree = {graph.average_degree()}')
    degs = graph.degrees()
    x = [d for d in degs.keys()]
    y = [c for c in degs.values()]
    plt.scatter(x, y)
    plt.show()


def draw_spectrum(graphs):
    s = np.array([nx.laplacian_spectrum(graph.to_nx()) for graph in graphs]).flatten()
    s = 1. / np.fromiter((x for x in s if .1 <= x <= 1), dtype=s.dtype)
    sns.distplot(s, bins=100)
    plt.show()


def np_dot():
    x = np.array([0, 1])
    y = np.array([1, 0])
    m = np.array([[1, 2], [3, 4]])
    print(x.dot(m))
    print(y.dot(m))
    print(x.dot(m).dot(y.T))
    print(x.dot(m).dot(y.T))
    print(x.dot(m.dot(y.T)))


if __name__ == '__main__':
    np_dot()
    exit(0)
    # draw_small_world(10000, 20, .7)
    # graph = RandomRegular(100, 3)
    # graph = GraphByDegrees({3: 10, 5: 10, 7: 10})
    graphs = [GraphByDegrees({2: 500, 3: 500}) for _ in range(100)]
    draw_spectrum(graphs)
    exit(0)

    G = nx.Graph()
    G.add_edges_from(graph.E)
    plt.subplot()
    nx.draw(G)
    plt.show()


