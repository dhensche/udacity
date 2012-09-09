__author__ = 'Derek'

from utils.graph import clustering_coefficient, make_link

def test():
    flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
        ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
        ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]

    G = {}
    for (x,y) in flights: make_link(G,x,y)

    assert clustering_coefficient(G) == 2.0/9.0

print test()