import random
import numpy as np
from graph import *
from viz import draw_contour, draw_contour_slow
from utils import Timer


if __name__ == '__main__':
    n = 1000
    p = 4. / n
    # graph = ErdosRenyi(n, p)
    # graph = Grid(40, 40)
    graph = ScaleFree(1000, 3)

    alphas = np.arange(0.01, 0.16, 0.02)
    bs = np.arange(3, 10, .25)

    for i in range(1, 65):
        timer = Timer()
        draw_contour(graph, bs, alphas, pool_size=i)
        print(f'pool size = {i}', end=' ')
        timer.print_elapsed()
