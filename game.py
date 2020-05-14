class PrisonerDilemma:
    def __init__(self, b, c):
        self.b = b
        self.c = c
        self.p = dict()
        self.p['CC'] = [b - c, b - c]
        self.p['CD'] = [-c, b]
        self.p['DC'] = [b, -c]
        self.p['DD'] = [0, 0]

    def payoff(self, *args):
        x, y = args
        if x not in 'CD':
            raise Exception(f'Got {x}!')
        if y not in 'CD':
            raise Exception(f'Got {y}!')
        return self.p[x + y]


