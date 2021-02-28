import networkx as nx
from graph import GraphByDegrees, ErdosRenyi
import matplotlib.pyplot as plt
import numpy as np


def get_b_stars(graph: nx.Graph):
    cnt = {}
    for u, v in graph.edges():
        du = graph.degree(u)
        dv = graph.degree(v)
        if du > dv:
            du, dv = dv, du
        if not (du, dv) in cnt:
            cnt[(du, dv)] = 0
        cnt[(du, dv)] += 1

    weights = {}
    for (du, dv), freq in cnt.items():
        for av in range(0, dv + 1):
            for bv in range(0, dv + 1):
                for au in range(0, du + 1):
                    for bu in range(0, du + 1):
                        den = bv * du - bu * dv
                        if den != 0:
                            ratio = (av * du - au * dv) / (bv * du - bu * dv)
                            if ratio not in weights:
                                weights[ratio] = 0
                            weights[ratio] += freq
    return weights


if __name__ == '__main__':
    graph = GraphByDegrees({2: 5000, 3: 5000})
    # graph = ErdosRenyi(1000, 5 / 1000)
    ratios = get_b_stars(graph)
    ratios = {k: v for k, v in ratios.items() if 1 < k <= 10}
    # plt.hist(list(ratios.keys()), weights=list(ratios.values()), bins=100)
    xs = np.linspace(1, 10, 100)

    total = sum(ratios.values())
    print('total =', total)
    print(ratios)

    def f(x):
        res = 0
        for k, v in ratios.items():
            if k <= x:
                res += v
        return res / total

    ys = [f(x) for x in xs]
    plt.plot(xs, ys)
    plt.show()

