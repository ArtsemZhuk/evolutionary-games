from multiprocessing import Pool
import random


def fun(n):
    a = [i for i in range(1, n + 1)]
    for i in range(n):
        for j in range(1, n):
            if random.uniform(0, 1) < 0.1:
                a[j] += a[j - 1]
    return sum(a)


def run(n, pool_size=4):
    pass

if __name__ == '__main__':
    run()
