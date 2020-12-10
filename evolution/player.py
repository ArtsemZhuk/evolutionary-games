class Player:
    def __init__(self, id):
        self.id = id
        self.prob = 0
        self.best_s = ''
        self.g_avg = 0
        self.deg = 0
        self.cnt = 0

    def sz(self):
        return max(1, self.deg)

    def coop_rate(self):
        return self.cnt / self.sz()

    def rigidity(self):
        return 1 - abs(1 - 2 * self.coop_rate())

