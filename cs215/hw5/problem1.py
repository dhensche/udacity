import heapq
import time

__author__ = 'Derek'

from utils.graph import make_link
from utils.heap import heap, priority_dict
#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
#

def dijkstra_mine(G,v):
    dist_so_far, final_dist = priority_dict(initial_dict={v:0}), {}
    for (w, d) in dist_so_far:
        if w in final_dist: continue
        final_dist[w] = d
        for x in G[w]:
            if x not in final_dist:
                new_dist = final_dist[w] + G[w][x]
                if x not in dist_so_far or new_dist < dist_so_far[x]:
                    dist_so_far[x] = new_dist
    return final_dist


def dijkstra(G,v):
    final_dist, dist_queue, dist_heap = {}, {v: 0}, [(0, v)]
    while dist_queue:
        distance, head = heapq.heappop(dist_heap)
        if head in final_dist or (head in dist_queue and dist_queue[head] < distance): continue
        final_dist[head] = distance
        del dist_queue[head]

        for successor in G[head]:
            if successor not in final_dist:
                new_weight = final_dist[head] + G[head][successor]
                if successor not in dist_queue or dist_queue[successor] > new_weight:
                    dist_queue[successor] = new_weight
                    heapq.heappush(dist_heap, (new_weight, successor))
    return final_dist

############
#
# Test


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3),
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    start = time.clock()
    dist = dijkstra(G, a)
    print str(time.clock() - start)
    start = time.clock()
    dist = dijkstra_mine(G, a)
    print str(time.clock() - start)
    print dist
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)


test()



