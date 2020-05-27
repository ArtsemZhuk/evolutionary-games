import numpy as np


class PrisonerDilemma:
    def __init__(self, b, c):
        self.b = b
        self.c = c
        self.p = dict()
        self.p['CC'] = [b - c, b - c]
        self.p['CD'] = [-c, b]
        self.p['DC'] = [b, -c]
        self.p['DD'] = [0, 0]

        self.matrix = np.array([[b - c, -c], [b, 0]], dtype=np.float)

    def payoff(self, *args):
        x, y = args
        if x not in 'CD':
            raise Exception(f'Got {x}!')
        if y not in 'CD':
            raise Exception(f'Got {y}!')
        return self.p[x + y]

    def mixed_payoff(self, x, y):
        px = x.dot(self.matrix).dot(y.T)
        py = y.dot(self.matrix).dot(x.T)
        return px, py



