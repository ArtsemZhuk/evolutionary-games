import numpy as np
import matplotlib.pyplot as plt

from graph import *
from utils import Timer
from viz import draw_contour, draw_data
from engine import fun
from engine_exp import fun_exp
from engine_mono import fun_mono
from engine_sum import fun_sum


if __name__ == '__main__':
    n = 1000
    p = 4. / n
    graph = ErdosRenyi(n, p)
    # graph = Grid(40, 40)
    # graph = ScaleFree(10, 3)

    timer = Timer()

    sets = dict()
    for v in graph.V:
        d = graph.deg(v)
        if d not in sets:
            sets[d] = []
        sets[d].append(v)
    sets['all'] = graph.V

    # res = fun((graph, 4, .1, 1000, '01', sets))
    res = fun_mono((graph, 3, .1, 300, '01', sets))
    # res = fun_sum((graph, 5, .025, 100))
    timer.print_elapsed()
    # plt.plot(res)
    for d in range(20):
        if d in sets and len(sets[d]) >= 20:
            plt.plot(res[d], label=d)
    plt.plot(res['all'], label='all')
    plt.legend()
    plt.show()
    exit(0)

    alphas = np.arange(0.01, 0.16, 0.01)
    bs = np.arange(3, 10, .08)
    T = 2

    timer = Timer()
    cz = list(map(np.mean, draw_contour(graph, bs, alphas, T, pool_size=4)))
    draw_data(bs, alphas, cz, levels=[.5, .7, .9])
    timer.print_elapsed()
