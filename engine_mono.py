import random

from game import PrisonerDilemma
from utils import mix_strategies
from mixed_player import MixedPlayer
import numpy as np

INF = 10 ** 18


def run(graph, game, alpha, T, init_type='uniform', sets=dict()):
    n = len(graph.V)
    # players = dict([(i, MixedPlayer(id=i)) for i in graph.V])
    players = [MixedPlayer(id=i) for i in graph.V]

    # TODO move init to arguments
    for p in players:
        if init_type == 'uniform':
            prob = random.uniform(0, 1)
            p.mixed_s = np.array([prob, 1 - prob], dtype=np.float)
        elif init_type == '01':
            prob = random.choice([0, 1])
            p.mixed_s = np.array([prob, 1 - prob], dtype=np.float)

        p.deg = graph.deg(p.id)

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for _ in range(T):
        for p in players:
            p.sum_half = np.zeros_like(p.mixed_s)
            p.best_g = -INF
            p.best_s = np.array([])

        for u, v in graph.E:
            players[u].sum_half += players[v].mixed_s
            players[v].sum_half += players[u].mixed_s

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

        for key, set in sets.items():
            rate = sum(players[id].coop_rate() for id in set) / max(len(set), 1)
            rates[key].append(rate)
    return rates


def fun_mono(tuple):
    # TODO add norm var
    graph, b, alpha, T, init_type, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T, init_type, sets)
    return rates
