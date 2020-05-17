import matplotlib.pyplot as plt
import numpy as np

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


if __name__ == '__main__':
    draw_small_world(10000, 20, .7)

