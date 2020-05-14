import random


class Graph:
    def __init__(self):
        self.V = []
        self.E = []
        self.N = dict()

    def add_vertices(self, vs):
        for v in vs:
            self.V.append(v)
            self.N[v] = []

    def add_edge(self, u, v):
        if not u in self.V or not v in self.V:
            raise Exception(f"{u} or {v} no present in {self.V}")

        if (u, v) in self.E or (v, u) in self.E:
            return

        self.E.append((u, v))
        self.N[u].append(v)
        self.N[v].append(u)

    def density(self):
        n = len(self.V)
        return len(self.E) / (n * (n - 1) // 2)

    def average_degree(self):
        return 2 * len(self.E) / len(self.V)

    def deg(self, v):
        return len(self.N[v])

    def degrees(self):
        ans = dict()
        for v in self.V:
            d = self.deg(v)
            ans[d] = ans.get(d, 0) + 1
        return ans


def ErdosRenyi(n, p):
    graph = Graph()
    graph.add_vertices(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if random.uniform(0, 1) < p:
                graph.add_edge(i, j)
    return graph


def FullGraph(n):
    return ErdosRenyi(n, 1.1)


def Circle(n):
    graph = Graph()
    graph.add_vertices(range(n))
    for i in range(n):
        j = (i + 1) % n
        graph.add_edge(i, j)
    return graph


def ScaleFree(n, m):
    graph = FullGraph(m + 1)
    us = [v for _ in range(m) for v in graph.V]
    for v in range(m + 1, n):
        neighbours = set()
        while len(neighbours) < m:
            to = random.choice(us)
            neighbours.add(to)
            # TODO think how optimize!

        graph.add_vertices([v])
        for u in neighbours:
            graph.add_edge(u, v)
            us.append(u)
            us.append(v)

    # print(f'len us = {len(us)}')

    return graph


def MultiGrid(ns):
    pass


def Grid(n, m):
    graph = Graph()
    graph.add_vertices([(i, j) for i in range(n) for j in range(m)])
    for i in range(n):
        for j in range(m):
            for dx, dy in [(-1, 0), (0, +1), (+1, 0), (0, -1)]:
                ti = (i + dx) % n
                tj = (j + dy) % m
                graph.add_edge((i, j), (ti, tj))
    return graph
