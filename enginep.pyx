# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from random import uniform, randint
from cython.parallel import parallel, prange
from graph import ErdosRenyi
from itertools import product

cdef extern from "stdlib.h":
    int rand() nogil

cdef extern from "math.h":
    double exp(double x) nogil

cdef double sigmoid(double x) nogil:
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1.0 / (1.0 + exp(-x))

cdef double rnd() nogil:
    cdef double x = rand()
    return x / 2147483647

cdef vector[double] run(vector[vector[int]] graph, vector[vector[double]] game, double alpha, int T) nogil:
    cdef int n = graph.size()
    cdef vector[vector[char]] strat = vector[vector[char]](n, vector[char](n, 0))
    cdef vector[vector[double]] g = vector[vector[double]](n, vector[double](n, 0))
    cdef vector[double] prob = vector[double](n, 0)
    cdef vector[double] g_avg = vector[double](n, 0)
    cdef vector[char] best_s = vector[char](n, 0)
    cdef char su, sv, cur_best_s
    cdef double pu, pv, cg
    # cdef double[2] cnt
    cdef double best, delta, r, cr
    cdef vector[double] coop_rates = vector[double](T)

    for i in range(n):
        for to in graph[i]:
            strat[i][to] = rand() % 2

    for it in range(T):
        for v in range(n):
            for u in graph[v]:
                sv = strat[v][u]
                su = strat[u][v]
                pv = game[sv][su]
                pu = game[su][sv]
                g[v][u] = pv
                g[u][v] = pu

        # cnt[0] = cnt[1] = 0

        for v in range(n):
            g_avg[v] = 0
            for u in graph[v]:
                g_avg[v] += g[v][u]
            g_avg[v] /= max(1, graph[v].size())

        for v in range(n):
            best = -1e18
            cur_best_s = -1
            for u in graph[v]:
                cg = g_avg[u]
                if best < cg:
                    best = cg
                    cur_best_s = strat[u][v]

            delta = (best - g_avg[v])
            prob[v] = sigmoid(delta / alpha)
            # cnt[cur_best_s] += 1
            best_s[v] = cur_best_s

        for v in range(n):
            for u in graph[v]:
                if rnd() < prob[v]:
                    strat[v][u] = best_s[v]

        r = 0
        for v in range(n):
            cr = 0
            for u in graph[v]:
                if strat[v][u] == 0:
                    cr += 1
            cr /= max(1, graph[v].size())
            r += cr
        r /= n
        coop_rates[it] = r
    return coop_rates

cdef vector[vector[double]] make_game(double b):
    cdef double c = 1
    cdef vector[vector[double]] game
    game.resize(2)
    game[0].resize(2)
    game[1].resize(2)
    cb = b / b
    cc = c / b
    game[0][0] = cb - cc
    game[0][1] = -cc
    game[1][0] = cb
    game[1][1] = 0
    return game

cdef vector[vector[int]] make_graph(graph):
    cdef vector[vector[int]] g = vector[vector[int]](len(graph.V))
    for u, v in graph.E:
        g[u].push_back(v)
    return g

def calc(alphas, bs, T, I, n, p, num_threads=32):
    cdef vector[vector[double]] cur_res
    cdef int j
    cdef vector[vector[vector[double]]] games
    cdef vector[vector[int]] g
    cdef double cb, cc
    cdef vector[pair[double, double]] grid
    cdef int TT
    res = []
    for i in range(I):
        graph = ErdosRenyi(n, p)
        g = make_graph(graph)
        games.clear()
        grid.clear()
        for (a, b) in product(alphas, bs):
            grid.push_back([a, b])
            games.push_back(make_game(b))
        cur_res = vector[vector[double]](len(grid))

        TT = T
        with nogil, parallel(num_threads=num_threads):
            for j in prange(grid.size()):
                cur_res[j] = run(g, games[j], grid[j].first, TT)
        res.append(list(cur_res))
    return res
