__author__ = 'Derek'

import utils.graph as graph

def test():
    flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
        ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
        ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]

    G = {}
    for (x,y) in flights: graph.make_link(G,x,y)
    marvel_G = graph.read_graph("resources/marvel_graph.tsv")


    assert graph.clustering_coefficient(G) == 2.0/9.0
    assert len(marvel_G) == 19255
    assert graph.path(marvel_G, 'A', 'ZZZAX') == ['A', 'W2 159', 'WOLVERINE/LOGAN ', 'W2 41', 'SUMMERS, NATHAN CHRI', 'C2 59', 'ZZZAX']
    assert graph.centrality(marvel_G, 'A') == 6
    return True

print test()

