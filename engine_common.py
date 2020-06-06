import random
import numpy as np

from mixed_player import MixedPlayer


def init_mixed_players(n, init_type, graph):
    players = [MixedPlayer(id=i) for i in range(n)]
    for p in players:
        if init_type == 'uniform':
            prob = random.uniform(0, 1)
            p.mixed_s = np.array([prob, 1 - prob], dtype=np.float)
        elif init_type == '01':
            prob = random.choice([0, 1])
            p.mixed_s = np.array([prob, 1 - prob], dtype=np.float)

        p.deg = graph.deg(p.id)
    return players


def store_rates(rates, players, sets):
    for key, set in sets.items():
        def getter(p):
            if str(key).startswith('l'):
                return p.rigidity()
            else:
                return p.coop_rate()
        rate = sum(getter(players[id]) for id in set) / max(len(set), 1)
        rates[key].append(rate)
