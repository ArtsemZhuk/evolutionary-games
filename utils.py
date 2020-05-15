import time
import math

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


