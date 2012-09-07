__author__ = 'dhensche'

# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

def find_eulerian_tour(graph):
    # your code here
    def find_tour(u):
        for (x, v) in graph:
            if x == u or v == u:
                graph.remove((x, v))
                return [u] + find_tour(v) if x == u else [v] + find_tour(x)
        return [u]

    full_tour = []
    while len(graph):
        tour = find_tour(graph[0][0])
        if tour[0] != tour[-1]: return []
        if len(full_tour):
            j, i = None, 0
            while j == None:
                try:
                    j = full_tour.index(tour[i])
                except ValueError:
                    i += 1
            full_tour = full_tour[:j] + tour[i:] + (tour[:i - 1] + full_tour[j:] if i != 0 else full_tour[j + 1:])
        else:
            full_tour = tour
    return full_tour

print find_eulerian_tour([(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)])
print find_eulerian_tour([(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)])
print find_eulerian_tour([(1, 13), (1, 6), (6, 11), (3, 13), (8, 13), (0, 6), (8, 9),(5, 9), (2, 6), (6, 10), (7, 9), (1, 12), (4, 12), (5, 14), (0, 1), (2, 3), (4, 11), (6, 9), (7, 14), (10, 13)])
print find_eulerian_tour([(8, 16), (8, 18), (16, 17), (18, 19), (3, 17), (13, 17), (5, 13),(3, 4), (0, 18), (3, 14), (11, 14), (1, 8), (1, 9), (4, 12), (2, 19),(1, 10), (7, 9), (13, 15), (6, 12), (0, 1), (2, 11), (3, 18), (5, 6), (7, 15), (8, 13), (10, 17)])

