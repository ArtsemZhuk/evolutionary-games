import random
from utils import sigmoid, pack_to_tuple
from player import Player
from game import PrisonerDilemma

INF = 10 ** 18


def run(graph, game, alpha, T):
    n = len(graph.V)
    players = dict([(i, Player(id=i)) for i in graph.V])

    # TODO move init to arguments
    for p in players.values():
        p.op = graph.N[p.id]
        for other in p.op:
            p.k[other] = random.choices(['C', 'D'], weights=[1, 1])[0]
            p.g[other] = 0

    coop_rates = []

    for _ in range(T):
        for u, v in graph.E:
            su = players[u].k[v]
            sv = players[v].k[u]
            pu, pv = game.payoff(su, sv)
            players[u].g[v] = pu
            players[v].g[u] = pv

        cnt = dict()

        for p in players.values():
            p.g_avg = sum(p.g.values()) / p.sz()

        for p in players.values():
            best = -INF
            best_s = ''
            for other in p.op:
                g = players[other].g_avg
                if best < g:
                    best = g
                    best_s = players[other].k[p.id]
            if best_s == '' and len(p.op) != 0:
                raise Exception(f'Not found best! u = {p.id} len = {len(p.op)}')

            delta = (best - p.g_avg)
            # TODO b = 1 ensure ????
            prob = sigmoid(delta / alpha)
            cnt[best_s] = cnt.get(best_s, 0) + 1

            p.prob = prob
            p.best_s = best_s

        # print(f'cnt = {cnt}')

        for p in players.values():
            for other in p.op:
                if random.uniform(0, 1) < p.prob:
                    p.k[other] = p.best_s

        r = [p.coop_rate() for p in players.values()]
        r_avg = sum(r) / n
        coop_rates.append(r_avg)
    return coop_rates


def fun(tuple):
    graph, b, alpha = tuple
    c = 1
    game = PrisonerDilemma(b / b, c / b)
    T = 100
    rates = run(graph, game, alpha, T)
    return rates[-1]
