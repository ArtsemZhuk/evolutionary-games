import random
import numpy as np
from graph import *
from viz import draw_contour, draw_contour_slow
from game import PrisonerDilemma
from utils import Timer
import math
import os
import multiprocessing

INF = 10 ** 18


class Player:
    def __init__(self, id):
        self.k = dict()
        self.g = dict()
        self.op = dict()
        self.id = id
        self.prob = 0
        self.best_s = ''
        self.g_avg = 0

    def sz(self):
        return max(1, len(self.k))

    def coop_rate(self):
        cnt = 0
        for key in self.k.values():
            if key == 'C':
                cnt += 1
        return cnt / self.sz()


def sigmoid(x):
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1. / (1 + math.exp(-x))


def run(graph, game, alpha, T):
    n = len(graph.V)
    players = dict([(i, Player(id=i)) for i in graph.V])

    # TODO move init to arguments
    for p in players.values():
        p.op = graph.N[p.id]
        for other in p.op:
            p.k[other] = random.choices(['C', 'D'], weights=[1, 1])[0]
            p.g[other] = 0

    coop_rates = []

    for _ in range(T):
        for u, v in graph.E:
            su = players[u].k[v]
            sv = players[v].k[u]
            pu, pv = game.payoff(su, sv)
            players[u].g[v] = pu
            players[v].g[u] = pv

        cnt = dict()

        for p in players.values():
            p.g_avg = sum(p.g.values()) / p.sz()

        for p in players.values():
            best = -INF
            best_s = ''
            for other in p.op:
                g = players[other].g_avg
                if best < g:
                    best = g
                    best_s = players[other].k[p.id]
            if best_s == '' and len(p.op) != 0:
                raise Exception(f'Not found best! u = {p.id} len = {len(p.op)}')

            delta = (best - p.g_avg)
            # TODO b = 1 ensure ????
            prob = sigmoid(delta / alpha)
            cnt[best_s] = cnt.get(best_s, 0) + 1

            p.prob = prob
            p.best_s = best_s

        # print(f'cnt = {cnt}')

        for p in players.values():
            for other in p.op:
                if random.uniform(0, 1) < p.prob:
                    p.k[other] = p.best_s

        r = [p.coop_rate() for p in players.values()]
        r_avg = sum(r) / n
        coop_rates.append(r_avg)
    return coop_rates


if __name__ == '__main__':
    n = 1000
    p = 4. / n
    # graph = ErdosRenyi(n, p)
    # graph = Grid(40, 40)
    graph = ScaleFree(1000, 3)

    alphas = np.arange(0.01, 0.16, 0.02)
    bs = np.arange(3, 10, .25)

    @np.vectorize
    def fun(b, alpha):
        c = 1
        game = PrisonerDilemma(b / b, c / b)
        T = 100
        rates = run(graph, game, alpha, T)
        return rates[-1]

    # os.system("taskset -p 0xff %d" % os.getpid())
    # pool_size = multiprocessing.cpu_count()
    # os.system('taskset -cp 0-%d %s' % (pool_size, os.getpid()))

    timer = Timer()
    draw_contour_slow(bs, alphas, fun)
    # print(f'pool size = {4}', end=' ')
    timer.print_elapsed()
