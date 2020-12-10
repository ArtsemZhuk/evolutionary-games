import random

from game import PrisonerDilemma
from player import Player
from engine_common import store_rates

import numpy as np

INF = 10 ** 18


def run(graph, game, alpha, T, sets=dict()):
    n = len(graph.V)
    players = [Player(id=i) for i in graph.V]

    # TODO vary init
    sus = random.choices([0, 1], k=len(graph.E))
    svs = random.choices([0, 1], k=len(graph.E))

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for p in players:
        p.deg = graph.deg(p.id)

    for _ in range(T):
        for p in players:
            p.g_avg = .0

        for (u, v), su, sv in zip(graph.E, sus, svs):
            pu, pv = game.payoff(su, sv)
            players[u].g_avg += pu
            players[v].g_avg += pv

        for p in players:
            p.prob = [.0, .0]
            p.g_avg /= p.sz()
            p.rem = np.exp(p.g_avg / alpha)

        for (u, v), su, sv in zip(graph.E, sus, svs):
            players[u].prob[sv] += players[v].rem
            players[v].prob[su] += players[u].rem

        for i in range(len(graph.E)):
            u, v = graph.E[i]

            prob_u = (players[u].prob[0] + (players[u].rem if sus[i] == 0 else 0)) \
                     / (sum(players[u].prob) + players[u].rem)
            if random.uniform(0, 1) < prob_u:
                sus[i] = 0
            else:
                sus[i] = 1

            prob_v = (players[v].prob[0] + (players[v].rem if svs[i] == 0 else 0)) \
                     / (sum(players[v].prob) + players[v].rem)
            if random.uniform(0, 1) < prob_v:
                svs[i] = 0
            else:
                svs[i] = 1

        for p in players:
            p.cnt = 0

        for (u, v), su, sv in zip(graph.E, sus, svs):
            players[u].cnt += 1 - su
            players[v].cnt += 1 - sv

        store_rates(rates, players, sets)

    return rates


def fun_tot(tuple):
    graph, b, alpha, T, _, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T, sets)
    return rates
