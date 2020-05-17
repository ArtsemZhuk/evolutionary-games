import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
from utils import Timer
from engine import fun


def draw_data(x, y, cz):
    z = np.reshape(cz, [len(y), len(x)])
    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, z, levels=100)
    fig.colorbar(cs, ax=ax)
    plt.show()


def draw_contour_slow(x, y, f):
    X, Y = np.meshgrid(x, y)
    z = f(X, Y)
    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, z, levels=100)
    fig.colorbar(cs, ax=ax)
    plt.show()


if __name__ == '__main__':
    x = np.arange(-100, 100, .5)
    y = np.arange(-100, 100, .5)

    def g(x, y):
        return x * y + y * y * y

    def h(x, y):
        return np.sin(x) * np.cos(y)

    for i in range(1, 11):
        timer = Timer()
        draw_contour(x, y, h, pool_size=i)
        print(f'pool size = {i}', end=' ')
        timer.print_elapsed()

    exit(0)


