__author__ = 'Derek'
from utils.graph import make_link
# Generate a combination lock graph given a list of nodes
#

def create_combo_lock(nodes):
    G = {}
    prev = first = nodes[0]
    for node in nodes[1:]:
        make_link(G, first, node)
        if first != prev:
            make_link(G, prev, node)
        prev = node
    # your code here
    return G

##############
# Code for testing
#
def is_chain(graph, nodes):
    # find the first node with degree one
    start = (n for n, e in graph.iteritems()
        if len(e) == 1).next()
    count = 1
    # keep track of what we've seen to make
    # sure there are no cycles
    seen = set([start])
    # follow the edges
    prev = None
    current = start
    while True:
        nexts = graph[current].keys()
        # get rid of the edge back to prev
        nexts = [n for n in nexts if not n == prev]
        if len(nexts) > 1:
            # bad.  too many edges to be a chain
            return False
        elif len(nexts) == 0:
            # We're done following the chain
            # Did we get enough edges:
            return count == len(nodes)
        prev = current
        current = nexts[0]
        if current in seen:
            # bad.  this isn't a chain
            # it has a loop
            return False
        seen.add(current)
        count += 1

def is_combo_lock(graph, nodes):
    # first see if we have a star
    center = None
    degree = None
    for node, edges in graph.iteritems():
        if len(edges) > degree:
            center = node
            degree = len(edges)
    if not degree == len(nodes) - 1:
        return False
        # make a graph out of all the edges
    # not connected to the center
    chain = {}
    for node, edges in graph.iteritems():
        if node == center:
            continue
        for e in edges:
            if e == center:
                continue
            make_link(chain, node, e)
    return is_chain(chain, [n for n in nodes if n != center])

def test():
    for n in [5, 10, 20]:
        combo = create_combo_lock(range(n))
        if not is_combo_lock(combo, range(n)):
            return False
    return True

print test()