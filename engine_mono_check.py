import random

from game import PrisonerDilemma
from player import Player
from utils import sigmoid
from engine_common import store_rates

INF = 10 ** 18


def run(graph, game, alpha, T, sets=dict()):
    n = len(graph.V)
    players = [Player(id=i) for i in graph.V]

    # TODO vary init
    sus = random.choices([0., 1.], k=len(graph.E))
    svs = random.choices([0., 1.], k=len(graph.E))

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for p in players:
        p.deg = graph.deg(p.id)

    for _ in range(T):
        for p in players:
            p.g_avg = .0
            p.best_neighbor = -1

        for (u, v), su, sv in zip(graph.E, sus, svs):
            pu, pv = game.real_payoff(su, sv)
            players[u].g_avg += pu
            players[v].g_avg += pv

        for p in players:
            p.best_g = -INF
            p.best_s = None
            p.g_avg /= p.sz()

        for (u, v), su, sv in zip(graph.E, sus, svs):
            if players[u].best_g < players[v].g_avg:
                players[u].best_g = players[v].g_avg
                players[u].best_s = sv
                players[u].best_neighbor = v

            if players[v].best_g < players[u].g_avg:
                players[v].best_g = players[u].g_avg
                players[v].best_s = su
                players[v].best_neighbor = u

        for p in players:
            delta = (p.best_g - p.g_avg)
            # TODO b = 1 ensure ????
            p.prob = sigmoid(delta / alpha)
            print(f'{p.id} -> {p.prob} -> {p.best_s}')

        print(sus)
        for i in range(len(graph.E)):
            u, v = graph.E[i]
            # if random.uniform(0, 1) < players[u].prob:
            sus[i] = sus[i] * (1 - players[u].prob) + players[u].best_s * players[u].prob
            #if random.uniform(0, 1) < players[v].prob:
            svs[i] = svs[i] * (1 - players[v].prob) + players[v].best_s * players[v].prob

        # print(sus)

        for p in players:
            p.cnt = 0.

        for (u, v), su, sv in zip(graph.E, sus, svs):
            players[u].cnt += 1 - su
            players[v].cnt += 1 - sv

        store_rates(rates, players, sets)

    return rates


def fun_mono_check(tuple):
    graph, b, alpha, T, _, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T, sets)
    return rates
