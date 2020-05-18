from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
from sys import exit

from engine import fun
from utils import Timer


def draw_data(x, y, cz, levels=[]):
    z = np.reshape(cz, [len(y), len(x)])
    fig, ax = plt.subplots()
    CSF = ax.contourf(x, y, z, levels=100)
    CS = ax.contour(x, y, z, levels=levels, colors='black', linestyles='dashed')
    fig.colorbar(CSF, ax=ax)
    plt.show()


def draw_contour(graph, x, y, T, pool_size=4):
    p = Pool(pool_size)
    return p.map(fun, [(graph, a, b, T) for b in y for a in x])


def draw_contour_slow(x, y, f):
    X, Y = np.meshgrid(x, y)
    z = f(X, Y)
    fig, ax = plt.subplots()
    CSF = ax.contourf(x, y, z, levels=100)
    CS = ax.contour(x, y, z, levels=[-.5, .1, .5, .7], colors='black', linestyles='dashed')
    fig.colorbar(CSF, ax=ax)
    plt.clabel(CS, fmt='%1.1f', colors='k', fontsize=14)  # contour line labels

    plt.show()


if __name__ == '__main__':
    x = np.arange(-5, 5, .1)
    y = np.arange(-5, 5, .1)

    def g(x, y):
        return x * y + y * y * y

    def h(x, y):
        return np.sin(x) * np.cos(y)

    timer = Timer()
    draw_contour_slow(x, y, h)
    timer.print_elapsed()

    exit(0)


