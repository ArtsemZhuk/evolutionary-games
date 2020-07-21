import networkx as nx
import matplotlib.pyplot as plt
from graph import GraphByDegrees, move_assortativity, ErdosRenyi
import random


if __name__ == '__main__':
    for _ in range(1):
        graph = GraphByDegrees({5: 100, 7: 100})
        # graph = ErdosRenyi(200, 5. / 200.)
        move_assortativity(graph, +1000)

        print(nx.degree_pearson_correlation_coefficient(graph))

        nx.draw(graph, node_size=20)
        plt.show()

