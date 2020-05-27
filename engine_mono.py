import random

from game import PrisonerDilemma
from utils import mix_strategies
from mixed_player import MixedPlayer
import numpy as np

INF = 10 ** 18


def run(graph, game, alpha, T):
    n = len(graph.V)
    players = dict([(i, MixedPlayer(id=i)) for i in graph.V])

    # TODO move init to arguments
    for p in players.values():
        p.op = graph.N[p.id]
        prob = random.uniform(0, 1)
        p.mixed_strategy = np.array([prob, 1 - prob], dtype=np.float)
        for other in p.op:
            p.g[other] = 0

    coop_rates = []

    for _ in range(T):
        for u, v in graph.E:
            su = players[u].mixed_strategy
            sv = players[v].mixed_strategy
            pu, pv = game.mixed_payoff(su, sv)
            players[u].g[v] = pu
            players[v].g[u] = pv

        for p in players.values():
            p.g_avg = sum(p.g.values()) / p.sz()

        for p in players.values():
            best_g = -INF
            best_s = np.array([])
            for other in p.op:
                g = players[other].g_avg
                if best_g < g:
                    best_g = g
                    best_s = players[other].mixed_strategy
            if best_s == np.array([]) and len(p.op) != 0:
                raise Exception(f'Not found best! u = {p.id} len = {len(p.op)}')

            p.best_g = best_g
            p.best_s = best_s

        for p in players.values():
            if not p.empty():
                p.mixed_strategy = mix_strategies(p.g_avg, p.best_g, p.mixed_strategy, p.best_s)

        r = [p.coop_rate() for p in players.values()]
        r_avg = sum(r) / n
        coop_rates.append(r_avg)
    return coop_rates


def fun_mono(tuple):
    graph, b, alpha, T = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T)
    return rates
