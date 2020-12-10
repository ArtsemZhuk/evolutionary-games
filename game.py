import numpy as np


class PrisonerDilemma:
    def __init__(self, b, c):
        self.b = b
        self.c = c

        self.matrix = np.array([[b - c, -c], [b, 0]], dtype=np.float)

    def payoff(self, *args):
        x, y = args
        return self.matrix[x, y], self.matrix[y, x]

    def real_payoff(self, x, y):
        return (1-y) - (1-x) / self.b, (1-x) - (1-y) / self.b

    def mixed_payoff(self, x, y):
        px = x.dot(self.matrix).dot(y.T)
        py = y.dot(self.matrix).dot(x.T)
        return px, py



