import random

from game import PrisonerDilemma
from mixed_player import MixedPlayer
from engine_common import init_mixed_players, store_rates
import numpy as np

INF = 10 ** 18


def run(graph, game, alpha, T, init_type, sets):
    n = len(graph.V)

    players = init_mixed_players(n, init_type, graph)

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for _ in range(T):
        for p in players:
            p.sum_half = np.zeros_like(p.mixed_s)

        for u, v in graph.twoE():
            players[u].sum_half += players[v].mixed_s

        for p in players:
            p.sum_half /= p.sz()
            p.g_avg = p.mixed_s.dot(game.matrix).dot(p.sum_half.T)
            p.temp_s = p.mixed_s * np.exp(p.g_avg / alpha)
            p.mixed_s = np.array(p.temp_s)

        for u, v in graph.twoE():
            players[u].mixed_s += players[v].temp_s

        for p in players:
            p.mixed_s /= np.sum(p.mixed_s)

        store_rates(rates, players, sets)

    return rates


def fun_sum(tuple):
    graph, b, alpha, T, init_type, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T, init_type, sets)
    return rates
