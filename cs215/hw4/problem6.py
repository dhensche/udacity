from collections import deque
import csv
from utils import graph

__author__ = 'Derek'

def centrality2(G, v, mu = float("inf")):
    path_from_start = {}
    open_list = deque([v])
    s, n = 0.0, 1
    path_from_start[v] = 0
    while len(open_list) > 0:
        current = open_list.popleft()
        for neighbor in G[current].keys():
            if neighbor not in path_from_start:
                x = path_from_start[neighbor] = path_from_start[current] + 1
                s += x
                n += 1
                if s / n > mu:
                    return s / n
                open_list.append(neighbor)
    return s / n

tsv = csv.reader(open("resources/imdb-1.tsv"), delimiter='\t')
G, actors, movies = {}, set(), set()
for (actor, movie, year) in tsv:
    actors.add(actor)
    movies.add(movie)
    graph.make_link(G, actor, movie)

actors = list(actors)
movies = list(movies)

times2 = []
T20 = []
for actor in actors[:20]:
    T20.append((centrality2(G, actor), actor))

T20.sort()
for actor in actors[20:]:
    mu = centrality2(G, actor, T20[19][0])
    if mu < T20[19][0]:
        T20.append((mu, actor))
        T20.sort()
        T20.pop()

print T20
