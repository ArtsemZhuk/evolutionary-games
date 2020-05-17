import time
import math
from multiprocessing import Pool
from engine import fun


class Timer:
    def __init__(self):
        self.start = time.time()

    def reset(self):
        self.start = time.time()

    def measure(self):
        return time.time() - self.start

    def print_elapsed(self):
        print(f'time elapsed = {self.measure()}')


def pack_to_tuple(f):
    def g(tuple):
        return f(*tuple)
    return g


def sigmoid(x):
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1. / (1 + math.exp(-x))


def draw_contour(graph, x, y, T, pool_size=4):
    p = Pool(pool_size)
    return p.map(fun, [(graph, a, b, T) for b in y for a in x])


