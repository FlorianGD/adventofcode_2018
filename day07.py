"""AoC 2018 Day 7 The Sum of Its Parts"""

import networkx as nx
import matplotlib.pyplot as plt

# Part 1
# If I understand the problem correctly, we want a lexicographical topological
# sort for the graph (see networkx documentation).
# So we need to parse the input to get the graph, and then let networkx work


def input_to_graph(steps):
    """
    Parse input and return a directed graph (nx.DiGraph)
    """
    G = nx.DiGraph()
    for line in steps:
        # Get only the node names, they are only one letter long
        _, [before, *_], [after, *_] = line.split('tep ')
        G.add_edge(before, after)
    return G


def ordered_steps(G):
    """
    Returns the lexicographical topological sort of the graph
    """
    steps = nx.algorithms.dag.lexicographical_topological_sort(G)
    return ''.join(steps)


test_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()

test_graph = input_to_graph(test_input)
assert ordered_steps(test_graph) == "CABDFE"

with open('day07_input.txt') as f:
    day07 = f.readlines()

graph = input_to_graph(day07)
print(f'Solution for part 1: {ordered_steps(graph)}')
nx.draw(graph, with_labels=True)
plt.show()
