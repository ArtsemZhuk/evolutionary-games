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

    # os.system("taskset -p 0xff %d" % os.getpid())
    # pool_size = multiprocessing.cpu_count()
    # os.system('taskset -cp 0-%d %s' % (pool_size, os.getpid()))

    timer = Timer()
    draw_contour(graph, bs, alphas)
    # print(f'pool size = {4}', end=' ')
    timer.print_elapsed()
