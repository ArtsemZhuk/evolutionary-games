import numpy as np


class MixedPlayer:
    def __init__(self, id):
        self.id = id
        self.mixed_s = dict()
        self.best_g = 0
        self.best_s = np.array([0, 1])
        self.deg = 0

    def sz(self):
        return max(1, self.deg)

    def empty(self):
        return self.deg == 0

    def coop_rate(self):
        if isinstance(self.mixed_s, dict):
            return sum([t[0] for t in self.mixed_s.values()]) / self.sz()
        else:
            return self.mixed_s[0]

    def rigidity(self):
        return 1 - abs(1 - 2 * self.coop_rate())

