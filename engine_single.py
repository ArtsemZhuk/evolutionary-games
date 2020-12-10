import random
import networkx as nx

from game import PrisonerDilemma
from player import Player
from utils import sigmoid
from engine_common import store_rates

INF = 10 ** 18


def run(graph: nx.Graph, game, alpha, T, sets=dict()):
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    players = [Player(id=i) for i in graph.nodes()]

    # TODO vary init
    # strategy per node
    ss = random.choices([0, 1], k=n)

    rates = dict()
    for key in sets.keys():
        rates[key] = []

    for p in players:
        p.deg = graph.degree(p.id)

    for _ in range(T):
        for p in players:
            p.g_avg = .0
            p.sig = .0
            p.rho = .0
            p.best_neighbor = -1

        for u, v in graph.edges():
            su, sv = ss[u], ss[v]
            pu, pv = game.payoff(su, sv)
            players[u].g_avg += pu
            players[v].g_avg += pv

            players[u].sig += 1 - sv
            players[v].sig += 1 - su

            players[u].rho += 1 - su
            players[v].rho += 1 - sv

        for p in players:
            p.best_g = -INF
            p.best_s = None
            p.g_avg /= p.sz()

            p.sig /= p.sz()
            p.rho /= p.sz()

        for u, v in graph.edges():
            su, sv = ss[u], ss[v]
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
            if p.best_neighbor != -1:
                if random.uniform(0, 1) < p.prob:
                    ss[p.id] = p.best_s

        for p in players:
            p.cnt = 0

        for u, v in graph.edges():
            su, sv = ss[u], ss[v]
            players[u].cnt += 1 - su
            players[v].cnt += 1 - sv

        store_rates(rates, players, sets)

    return rates


def fun_single(tuple):
    graph, b, alpha, T, _, sets = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    rates = run(graph, game, alpha, T, sets)
    return rates
