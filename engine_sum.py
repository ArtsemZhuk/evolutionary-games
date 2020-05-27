import random

from game import PrisonerDilemma
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
        p.mixed_s = np.array([prob, 1 - prob], dtype=np.float)
        for other in p.op:
            p.g[other] = 0

    coop_rates = []

    for _ in range(T):
        for u, v in graph.E:
            su = players[u].mixed_s
            sv = players[v].mixed_s
            pu, pv = game.mixed_payoff(su, sv)
            players[u].g[v] = pu
            players[v].g[u] = pv

        for p in players.values():
            p.g_avg = sum(p.g.values()) / p.sz()
            p.temp_s = p.mixed_s * np.exp(p.g_avg / alpha)

        for p in players.values():
            p.mixed_s = np.array(p.temp_s)
            for other in p.op():
                p.mixed_s += p[other].temp_s
            p.mixed_s /= np.sum(p.mixed_s)

        r = [p.coop_rate() for p in players.values()]
        r_avg = sum(r) / n
        coop_rates.append(r_avg)
    return coop_rates


def fun_sum(tuple):
    graph, b, alpha, T = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T)
    return rates
