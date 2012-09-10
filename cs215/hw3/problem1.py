__author__ = 'dhensche'

import utils.graph as graph

a = [(1,2),(1,3),(1,4),(1,5),(1,6),(2,3),(2,6),(4,3),(4,5),(5,6)]
b = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(3,4),(6,7)]
c = [(1,2),(1,3),(1,4),(1,5),(1,6)]
d = [(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)]
e = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,2)]
f = [(1,2),(1,3),(1,4),(1,5),(1,6),(3,4),(4,5),(5,6)]

edges = {'a':a,'b':b,'c':c,'d':d,'e':e,'f':f}
graphs = {}
for (key, edge_list) in edges.iteritems(): graphs[key] = graph.make_graph(edge_list)

print ''.join(map(lambda y: y[1], sorted(map(lambda x: (graph.clustering_coefficient(x[1],1),x[0]), graphs.iteritems()))))