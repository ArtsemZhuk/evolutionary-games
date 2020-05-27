class Player:
    def __init__(self, id):
        self.k = dict()
        self.id = id
        self.prob = 0
        self.best_s = ''
        self.g_avg = 0

    def sz(self):
        return max(1, len(self.k))

    def coop_rate(self):
        cnt = 0
        for key in self.k.values():
            if key == 'C':
                cnt += 1
        return cnt / self.sz()

    def rigidity(self):
        return 1 - abs(1 - 2 * self.coop_rate())

