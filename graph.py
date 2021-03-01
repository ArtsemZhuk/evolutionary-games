import random
import networkx as nx


def ErdosRenyi(n, p):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if random.uniform(0, 1) < p:
                graph.add_edge(i, j)
    return graph


def FullGraph(n):
    return ErdosRenyi(n, 1.1)


def ScaleFree(n, m):
    graph = FullGraph(m + 1)
    us = [v for _ in range(m) for v in graph.nodes()]
    for v in range(m + 1, n):
        neighbours = set()
        while len(neighbours) < m:
            to = random.choice(us)
            neighbours.add(to)
            # TODO think how optimize!

        graph.add_node(v)
        for u in neighbours:
            graph.add_edge(u, v)
            us.append(u)
            us.append(v)

    return graph


def Circle(n, k=1):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
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
                    if j != i and j not in graph.neighbors(i):
                        break
                graph.add_edge(i, j)
    return graph


def MultiGrid(ns):
    pass


def Grid(n, m):
    graph = nx.Graph()
    graph.add_nodes_from([(i, j) for i in range(n) for j in range(m)])
    for i in range(n):
        for j in range(m):
            for dx, dy in [(-1, 0), (0, +1), (+1, 0), (0, -1)]:
                ti = (i + dx) % n
                tj = (j + dy) % m
                graph.add_edge((i, j), (ti, tj))
    return graph


def GraphByDegrees(degs, assortativity_inc=0):
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

        graph = nx.Graph()
        graph.add_nodes_from(range(n))

        good = True

        for i in range(0, len(a), 2):
            u = a[i]
            v = a[i + 1]
            if u == v or graph.has_edge(u, v):
                good = False
                break
            else:
                graph.add_edge(u, v)

        if good and nx.is_connected(graph):
            while assortativity_inc < 0:
                pass

            while assortativity_inc > 0:
                pass

            return graph


def quad_switch(graph: nx.Graph, u1, v1, u2, v2) -> bool:
    if not graph.has_edge(u1, v1) or not graph.has_edge(u2, v2):
        return False

    if graph.has_edge(u1, u2) or graph.has_edge(v1, v2):
        return False

    num_connected = nx.number_connected_components(graph)

    graph.remove_edge(u1, v1)
    graph.remove_edge(u2, v2)

    graph.add_edge(u1, u2)
    graph.add_edge(v1, v2)

    if nx.number_connected_components(graph) != num_connected:
        graph.remove_edge(u1, u2)
        graph.remove_edge(v1, v2)

        graph.add_edge(u1, v1)
        graph.add_edge(u2, v2)

        return False

    return True


def move_assortativity(graph: nx.Graph, by):
    fall_rate = 0
    for _ in range(abs(by)):
        # count = Counter([graph.degree(v) for v in graph.nodes()])
        # print(count)

        # if fall_rate >= 100:
        #    return

        # todo fix for more than two different degrees
        e = dict()
        for u, v in graph.edges():
            du = graph.degree(u)
            dv = graph.degree(v)

            if du > dv:
                u, v = v, u
                du, dv = dv, du

            d = du, dv

            if (by < 0) != (du == dv):
                continue

            if d not in e:
                e[d] = []
            e[d].append((u, v))

        good = True

        if by > 0:
            # todo fix
            key = random.choice(list(e.keys()))

            if len(e[key]) < 2:
                good = False
            else:
                e1 = random.choice(e[key])
                e[key].remove(e1)
                e2 = random.choice(e[key])
                e[key].remove(e2)
        else:

            if len(e) < 2:
                good = False
            else:
                keys = list(e.keys())

                key1 = random.choice(keys)
                keys.remove(key1)
                key2 = random.choice(keys)

                e1 = random.choice(e[key1])
                e2 = random.choice(e[key2])

        if good:
            u1, v1 = e1
            u2, v2 = e2
            if quad_switch(graph, u1, v1, u2, v2):
                by -= -1 if by < 0 else +1
            else:
                good = False

        if not good:
            fall_rate += 1


def RandomRegular(n, k):
    if n * k % 2 == 1 or n <= k:
        raise Exception(f'Can build regular graph with {n} vertices and deg {k}')
    return GraphByDegrees({k: n})


def ER(t):
    return ErdosRenyi(*t)


def SF(t):
    return ScaleFree(*t)


def WS(t):
    return SmallWorld(*t)


def er_graphs(cnt, n, k):
    for _ in range(cnt):
        yield ErdosRenyi(n, k / n)


def sf_graphs(cnt, n, m):
    for _ in range(cnt):
        yield ScaleFree(n, m)


def ws_graphs(cnt, n, k, beta):
    for _ in range(cnt):
        yield SmallWorld(n, k, beta)


def r_graphs(cnt, degs):
    for _ in range(cnt):
        yield GraphByDegrees(degs)


