from game import PrisonerDilemma
from utils import mix_strategies
from mixed_player import MixedPlayer
from engine_common import init_mixed_players, store_rates
import numpy as np

INF = 10 ** 18


def run(graph, game, alpha, T, init_type='uniform', sets=dict()):
    n = len(graph.V)

    players = init_mixed_players(n, init_type, graph)

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for _ in range(T):
        for p in players:
            p.sum_half = np.zeros_like(p.mixed_s)
            p.best_g = -INF
            p.best_s = np.array([])

        for u, v in graph.twoE():
            players[u].sum_half += players[v].mixed_s

        for p in players:
            p.sum_half /= p.sz()
            p.g_avg = p.mixed_s.dot(game.matrix).dot(p.sum_half.T)

        for u, v in graph.twoE():
            if players[u].best_g < players[v].g_avg:
                players[u].best_g = players[v].g_avg
                players[u].best_s = players[v].mixed_s

        for p in players:
            if not p.empty():
                p.mixed_s = mix_strategies(p.g_avg / alpha, p.best_g / alpha, p.mixed_s, p.best_s)

        store_rates(rates, players, sets)

    return rates


def fun_mono(tuple):
    # TODO add norm var
    graph, b, alpha, T, init_type, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T, init_type, sets)
    return rates
