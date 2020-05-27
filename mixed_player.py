import numpy as np


class MixedPlayer:
    def __init__(self, id):
        self.id = id
        self.op = dict()
        self.g = dict()
        self.mixed_s = dict()
        self.temp_s = np.array([0, 1])
        self.best_g = 0
        self.best_s = np.array([0, 1])
        self.half = np.array([])

    def sz(self):
        return max(1, len(self.op))

    def empty(self):
        return len(self.op) == 0

    def coop_rate(self):
        if isinstance(self.mixed_s, dict):
            return sum([t[0] for t in self.mixed_s.values()]) / self.sz()
        else:
            return self.mixed_s[0]

    def rigidity(self):
        return 1 - abs(1 - 2 * self.coop_rate())

