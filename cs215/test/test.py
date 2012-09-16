from utils.heap import heap
import utils.graph as graph

__author__ = 'Derek'

def test_heap():
    L = heap(reversed(range(10)))
    L.remove_min()
    assert L[0] == 1

    L = heap([2, 4, 3, 5, 9, 7, 7])
    L += [1]
    L.up_heapify(7)
    assert 1 == L[0]
    assert 2 == L[1]

def test_graph():
    flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
        ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
        ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]

    G = {}
    for (x,y) in flights: graph.make_link(G,x,y)
    marvel_G = graph.read_graph("resources/marvel_graph.tsv")


    assert graph.clustering_coefficient(G) == 2.0/9.0
    assert len(marvel_G) == 19255
    assert graph.path(marvel_G, 'A', 'ZZZAX') == ['A', 'W2 159', 'WOLVERINE/LOGAN ', 'W2 41', 'SUMMERS, NATHAN CHRI', 'C2 59', 'ZZZAX']
    assert 5.11 > graph.centrality(marvel_G, 'A') > 5.1

def test():
    test_graph()
    test_heap()
    return True

print test()

