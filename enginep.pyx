# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from random import uniform, randint
from math import exp

cdef double sigmoid(double x):
	if x > 100:
		return 1
	if x < -100:
		return 0
	return 1.0 / (1.0 + exp(-x))

cdef vector[double] run(vector[vector[int]] graph, vector[vector[pair[double, double]]] game, double alpha, int T):
	cdef int n = graph.size()
	cdef vector[vector[char]] strat = vector[vector[char]](n, vector[char](n, 0))
	cdef vector[vector[double]] g = vector[vector[double]](n, vector[double](n, 0))
	cdef vector[double] prob = vector[double](n, 0)
	cdef vector[double] g_avg = vector[double](n, 0)
	cdef vector[char] best_s = vector[char](n, 0)
	cdef char su, sv, cur_best_s
	cdef double pu, pv, cg
	cdef double[2] cnt
	cdef double best, delta, r, cr

	coop_rates = vector[double](T)
	for i in range(n):
		for to in graph[i]:
			strat[i][to] = randint(0, 1)

	for it in range(T):
		print(it)
		for i in range(n):
			for to in graph[i]:
				su = strat[i][to]
				sv = strat[to][i]
				pu = game[su][sv].first
				pv = game[su][sv].second
		cnt[0] = cnt[1] = 0
		for i in range(n):
			g_avg[i] = 0
			for to in graph[i]:
				g_avg[i] += g[i][to]
			g_avg[i] /= graph[i].size()
		for i in range(n):
			best = -1e18
			cur_best_s = -1
			for to in graph[i]:
				cg = g_avg[to]
				if best < cg:
					best = cg
					cur_best_s = strat[to][i]

			delta = (best - g_avg[i])
			prob[i] = sigmoid(delta / alpha)
			cnt[cur_best_s] += 1
			best_s[i] = cur_best_s

		for i in range(n):
			for to in graph[i]:
				if uniform(0, 1) < prob[i]:
					strat[i][to] = best_s[i]

		r = 0
		for i in range(n):
			cr = 0
			for to in graph[i]:
				if strat[i][to] == 0: cr += 1
			cr /= graph[i].size()
			r += cr
		r /= n
		coop_rates[it] = r
	return coop_rates

def fun(t):
	cdef vector[vector[pair[double, double]]] game
	cdef vector[vector[int]] g
	cdef double cb, cc
	graph, b, alpha, T = t
	c = 1

	game.resize(2)
	game[0].resize(2)
	game[1].resize(2)
	cb = b / b
	cc = c / b
	game[0][0] = [cb - cc, cb - cc]
	game[0][1] = [-cc, cb]
	game[1][0] = [cb, -cc]
	game[1][1] = [0, 0]

	g.resize(len(graph.V))
	for u, v in graph.E:
		g[u].push_back(v)

	return list(run(g, game, alpha, T))