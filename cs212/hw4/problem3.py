__author__ = 'dhensche'

# -----------------
# User Instructions
#
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... }
#
# For example, when calling subway(boston), one of the entries in the
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}.
# This means that foresthills only has one neighbor ('backbay') and
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and
# longest_ride function. ride(here, there, system) takes as input
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given
# subway system.

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and
# longest_ride() will be explicitly tested. If your code passes the
# assert statements in test_ride(), it should be marked correct.

def subway(**lines):
    sub = {}
    lines = dict((line, lines[line].split(' ')) for line in lines.keys())
    for line in lines.keys():
        num_of_stations = len(lines[line])
        for i in range(num_of_stations):
            station = lines[line][i]

            sub[station] = {} if sub.get(station) is None else sub[station]

            if i:
                sub[station][lines[line][i - 1]] = line
            if i + 1 < num_of_stations:
                sub[station][lines[line][i + 1]] = line

            for other_line in set(lines.keys()) - set([line]):
                if station in lines[other_line]:
                    num_of_other_stations = len(lines[other_line])
                    index = lines[other_line].index(station)
                    if index:
                        sub[station][lines[other_line][index - 1]] = other_line
                    if index + 1 < num_of_other_stations:
                        sub[station][lines[other_line][index + 1]] = other_line
    return sub

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')

def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."

    def successor(station):
        return system[station]

    return shortest_path_search(here, successor, lambda station: station == there)


def path_lenth(path):
    return len(path)


def longest_ride(system):
    return max([ride(start, stop) for start in system.keys() for stop in system.keys()], key=path_lenth)


def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [[start]] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []


def path_states(path):
    "Return a list of states in this path."
    return path[0::2]


def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]


def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or
            path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles',
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print boston
print ride('mit', 'government')
print test_ride()
