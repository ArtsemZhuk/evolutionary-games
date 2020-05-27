import numpy as np
import matplotlib.pyplot as plt

from graph import *
from utils import Timer
from viz import draw_contour, draw_data
from engine_exp import fun_exp


def run_exp(graph, b, alpha, T):
    res = fun_exp((graph, b, alpha, T))
    return res


if __name__ == '__main__':
    n = 100
    p = 4. / n
    graph = ErdosRenyi(n, p)
    # graph = Grid(40, 40)
    # graph = ScaleFree(10, 3)

    res = run_exp(graph, 5, .1, 100)
    print(res)
    plt.plot(res)
    plt.show()
    exit(0)

    alphas = np.arange(0.01, 0.16, 0.01)
    bs = np.arange(3, 10, .08)
    T = 2

    timer = Timer()
    cz = list(map(np.mean, draw_contour(graph, bs, alphas, T, pool_size=4)))
    draw_data(bs, alphas, cz, levels=[.5, .7, .9])
    timer.print_elapsed()
