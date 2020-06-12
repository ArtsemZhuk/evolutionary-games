import random
import networkx as nx


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
        if u not in self.V or v not in self.V:
            raise Exception(f"{u} or {v} no present in {self.V}")
        if u == v:
            raise Exception(f'Trying to make a loop over {u}!')

        if (u, v) in self.E or (v, u) in self.E:
            return

        self.E.append((u, v))
        self.N[u].append(v)
        self.N[v].append(u)

    def remove_edge(self, u, v):
        # TODO add checks
        self.N[u].remove(v)
        self.N[v].remove(u)
        if (u, v) in self.E:
            self.E.remove((u, v))
        elif (v, u) in self.E:
            self.E.remove((v, u))
        else:
            pass
            # TODO raise

    def twoE(self):
        for u, v in self.E:
            yield u, v
            yield v, u

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

    def to_nx(self):
        G = nx.Graph()
        G.add_edges_from(self.E)
        return G

    def max_degree(self):
        return max(self.deg(v) for v in self.V)


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

    return graph


def Circle(n, k=1):
    graph = Graph()
    graph.add_vertices(range(n))
    for i in range(n):
        for t in range(1, k + 1):
            j = (i + t) % n
            graph.add_edge(i, j)
    return graph


def SmallWorld(n, k, beta):
    graph = Circle(n, k // 2)
    for i in range(n):
        for t in range(1, k // 2 + 1):
            if random.uniform(0, 1) < beta: # TODO replace with bin variable, add to utils
                j = (i + t) % n
                graph.remove_edge(i, j)
                while True:
                    j = random.randint(0, n - 1)
                    if j != i and j not in graph.N[i]:
                        break
                graph.add_edge(i, j)
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


def is_connected(graph):
    p = [v for v in graph.V]

    def get(v):
        if p[v] != v:
            p[v] = get(p[v])
        return p[v]

    def uni(u, v):
        u = get(u)
        v = get(v)
        if u != v:
            p[u] = v

    for u, v in graph.E:
        uni(u, v)

    cnt = 0
    for v in graph.V:
        if p[v] == v:
            cnt += 1

    return cnt == 1


def GraphByDegrees(degs):
    a = []
    n = 0
    for d, cnt in degs.items():
        for i in range(cnt):
            a += [n] * d
            n += 1

    if len(a) % 2 != 0:
        raise Exception(f'sum of degrees uneven')

    while True:
        random.shuffle(a)

        graph = Graph()
        graph.add_vertices(range(n))

        good = True

        for i in range(0, len(a), 2):
            u = a[i]
            v = a[i + 1]
            if u == v or (u, v) in graph.E or (v, u) in graph.E:
                good = False
                break
            else:
                graph.add_edge(u, v)

        if good and is_connected(graph):
            return graph


def RandomRegular(n, k):
    if n * k % 2 == 1 or n <= k:
        raise Exception(f'Can build regular graph with {n} vertices and deg {k}')
    return GraphByDegrees({k : n})


