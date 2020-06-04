

def degs(graph, keys):
    sets = dict()
    for key in keys:
        sets[key] = []

    for v in graph.V:
        d = graph.deg(v)
        if d not in keys:
            continue
        sets[d].append(v)
    return sets


def coreness(graph, keys):
    sets = dict((k, []) for k in keys)

    n = len(graph.V)
    used = [False for _ in range(n)]

    mx = graph.max_degree()
    x = dict((i, []) for i in range(mx + 1))

    degs = [graph.deg(v) for v in range(n)]
    for v in range(n):
        x[degs[v]].append(v)

    c = [0] * n

    for cur in range(0, mx + 1):
        while len(x[cur]) > 0:
            v = x[cur].pop()
            if used[v]:
                continue

            used[v] = True
            c[v] = cur

            for u in graph.N[v]:
                if not used[u] and degs[u] > cur:
                    degs[u] -= 1
                    x[degs[u]].append(u)

    for v in range(n):
        if c[v] in keys:
            sets[c[v]].append(v)

    return sets



