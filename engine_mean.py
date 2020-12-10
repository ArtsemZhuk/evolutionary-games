import random

from game import PrisonerDilemma
from mixed_player import MixedPlayer
from engine_common import init_mixed_players, store_rates
import numpy as np

INF = 10 ** 18


def run(graph, b, alpha, T, init_type, sets):
    n = len(graph.V)

    players = init_mixed_players(n, init_type, graph)

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for _ in range(T):
        for p in players:
            p.mixed_s = p.mixed_s * np.exp(-p.mixed_s[0] / b / alpha)
            p.sum_half = np.zeros_like(p.mixed_s)
            p.sum_half += p.mixed_s

        for u, v in graph.twoE():
            players[u].sum_half += players[v].mixed_s

        for p in players:
            p.mixed_s = p.sum_half / sum(p.sum_half)

        store_rates(rates, players, sets)

    return rates


def fun_mean(tuple):
    graph, b, alpha, T, init_type, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, b, alpha, T, init_type, sets)
    return rates
