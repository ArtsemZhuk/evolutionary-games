import numpy as np
import matplotlib.pyplot as plt

from graph import *
from utils import Timer
from viz import draw_contour, draw_data
from engine import fun
from engine_exp import fun_exp
from engine_mono import fun_mono
from engine_sum import fun_sum
from engine_tot import fun_tot
from engine_mean import fun_mean
from engine_single import fun_single
from engine_mono_check import fun_mono_check
from graph_toolset import coreness, degs, biggest_degs
import seaborn as sns


def draw_corenees(graph):
    mx = graph.max_degree()
    keys = list(range(mx + 1))
    c = coreness(graph, keys)
    s = [i for i in keys for _ in c[i]]
    print(len(s))
    # sns.distplot(s, bins=10)
    fig, ax = plt.subplots()
    ax.hist(s)
    plt.show()


def draw_degrees(graph):
    mx = graph.max_degree()
    keys = list(range(mx + 1))
    c = degs(graph, keys)
    s = [i for i in keys for _ in c[i]]
    print(len(s))
    # sns.distplot(s, bins=10)
    fig, ax = plt.subplots()
    ax.hist(s)
    plt.show()


if __name__ == '__main__':
    n = 1000
    p = 4. / n
    graph = ErdosRenyi(n, p)
    # draw_corenees(graph)
    # draw_degrees(graph)
    # graph = Grid(40, 40)
    # graph = ScaleFree(1000, 4)
    # print(f'avg deg = {graph.average_degree()}')
    # exit(0)


    # star_sets = dict()
    # for key, value in sets.items():
    # for v in graph.nodes:
    #    star_sets[f'star{v}'] = [v]
    # print(star_sets)

    timer = Timer()

    # sets = coreness(graph, list(range(graph.max_degree() + 1)))
    # sets = {
        # 'l': list(range(n)),
    #    'rho': list(range(n))
    # }

    sets = dict()
    sets['rho'] = list(range(n))
    T = 1000

    res = fun_single((graph, 5, .1, T, '01', sets))
    # res = fun((graph, 5, .1, T, '01', star_sets))
    # res = fun_mono_check((graph, 100, .1, T, '01', sets))
    # res = fun_tot((graph, 20, .1, 1000, '01', sets))
    # res = fun_mono((graph, 5, .1, 1000, '01', sets))
    # res = fun_sum((graph, 4, .025, 100, '01', sets))
    # res = fun_mean((graph, 30, .1, 10, '01', sets))
    timer.print_elapsed()
    # plt.plot(res)
    for key in sets:
        if len(sets[key]) >= 1 and key != 'rho':
            plt.plot(res[key], label=key)
            # plt.scatter(list(range(T)), res[key], c='blue', alpha=.1, s=.1)
        elif key == 'rho':
            plt.plot(res[key], label=r'$\rho$')

    # plt.plot(res['all'], label='all')
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
