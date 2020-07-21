import numpy as np
import matplotlib.pyplot as plt

from graph import *
from utils import Timer
from viz import draw_contour, draw_data
from engine import fun
from graph_toolset import coreness, degs, biggest_degs



if __name__ == '__main__':
    n = 100
    p = 4. / n
    graph = ErdosRenyi(n, p)

    sets = dict()
    sets['rho'] = list(range(n))

    timer = Timer()

    T = 1000

    res = fun((graph, 5, .1, T, '01', sets))
    timer.print_elapsed()
    for key in sets:
        if len(sets[key]) >= 1 and key != 'rho':
            plt.plot(res[key], label=key)
        elif key == 'rho':
            plt.plot(res[key], label=r'$\rho$')

    plt.legend()
    plt.show()
