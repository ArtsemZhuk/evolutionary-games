import random

from game import PrisonerDilemma
from player import Player
from utils import sigmoid

INF = 10 ** 18


def run(graph, game, alpha, T):
    n = len(graph.V)
    players = [Player(id=i) for i in graph.V]

    # TODO move init to arguments
    for p in players:
        p.k = dict()
        for other in graph.N[p.id]:
            p.k[other] = random.choices(['C', 'D'], weights=[1, 1])[0]

    coop_rates = []

    for _ in range(T):
        for p in players:
            p.g_avg = .0

        for u, v in graph.E:
            su = players[u].k[v]
            sv = players[v].k[u]
            pu, pv = game.payoff(su, sv)
            players[u].g_avg += pu
            players[v].g_avg += pv

        for p in players:
            p.best_g = -INF
            p.best_s = None
            p.g_avg /= p.sz()

        for u, v in graph.twoE():
            if players[u].best_g < players[v].g_avg:
                players[u].best_g = players[v].g_avg
                players[u].best_s = players[v].k[u]

        for p in players:
            delta = (p.best_g - p.g_avg)
            # TODO b = 1 ensure ????
            p.prob = sigmoid(delta / alpha)
            for other in p.k.keys():
                if random.uniform(0, 1) < p.prob:
                    p.k[other] = p.best_s

        r = [p.coop_rate() for p in players]
        r_avg = sum(r) / n
        coop_rates.append(r_avg)
    return coop_rates


def fun(tuple):
    graph, b, alpha, T, _ = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T)
    return rates
