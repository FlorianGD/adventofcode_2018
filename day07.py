"""AoC 2018 Day 7 The Sum of Its Parts"""

import matplotlib.pyplot as plt
import networkx as nx

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

# Part 2
# We need to add a weight input to our graph. Then, I think we need to iterate
# through the graph manually to take into account the logic of the several
# workers.


def add_weight(G, offset=60):
    """
    Modify G inplace. The weights are 60 + 1 for A, 2 for B and so on.
    The offset parameter is just for testing purposes (it is 0 in the given
    example).
    """
    for node in G.nodes():
        G.nodes[node]['time'] = offset + ord(node) - 64


class Worker():
    """
    Simple class to handle a worker : is it available, what node does it work
    on, when will it be available.
    """
    def __init__(self, name):
        self.available = True
        self.name = name
        self.node = None
        self.remaining = 0

    def __repr__(self):
        return (f'Worker {self.name} on node {self.node} '
                f'with {self.remaining}s remaining')

    def work_on(self, node, time):
        self.available = False
        self.node = node
        self.remaining = time

    def update(self, time):
        self.remaining = max(0, self.remaining - time)
        if self.remaining == 0:
            self.available = True


class WorkerPool():
    """
    Handle a pool of workers.
    """
    def __init__(self, n_nworkers=5):
        self.n_workers = n_nworkers
        self.worker_list = [Worker(i) for i in range(n_nworkers)]
        self.time_elapsed = 0
        self.nodes_done = set()
        self.nodes_to_consider = set()

    def __repr__(self):
        return '\n'.join(repr(worker) for worker in self.worker_list)

    def assign_node(self, name, node, time):
        self.worker_list[name].work_on(node, time)
        self.nodes_to_consider.remove(node)

    def next_available(self):
        avail = [worker for worker in self.worker_list if worker.available]
        if avail:
            return avail[0]
        return min(self.worker_list, key=lambda worker: worker.remaining)

    def min_positive_time(self):
        mini = 200
        for worker in self.worker_list:
            if worker.remaining > 0 and worker.remaining < mini:
                mini = worker.remaining
        if mini == 200:
            return 0
        return mini

    def update_all(self, time):
        self.time_elapsed += time
        for worker in self.worker_list:
            worker.update(time)
            if worker.remaining == 0 and worker.node is not None:
                self.nodes_done.add(worker.node)
                worker.node = None

    def find_next_node(self, G):
        """
        Find the next available node
        """
        for node in sorted(self.nodes_to_consider):
            predecessor = list(G.predecessors(node))
            # If all the predecessors are in the set nodes_done
            # or if the nodes has no predecessor
            if set(predecessor).issubset(self.nodes_done):
                return node


def walk_graph(G, n_workers=5):
    """
    Using n_workers, walk through the graph. Returns the total time elapsed.
    The graph is already weighted.
    """
    all_nodes = set(G.nodes)
    pool = WorkerPool(n_nworkers=n_workers)
    next_worker = pool.next_available()
    # Find roots
    roots = sorted([node for node, d in G.in_degree() if d == 0])
    pool.nodes_to_consider = set(roots)

    # pool.assign_node(next_worker.name, next_node, G.nodes[next_node]['time'])
    # Iterate on the graph
    # pool.nodes_to_consider |= set(G.successors(next_node))
    while pool.nodes_done != all_nodes:
        next_node = pool.find_next_node(G)
        if next_node is None:
            # No node available, consume the remaining time
            time = pool.min_positive_time()
            pool.update_all(time)
        else:
            next_worker = pool.next_available()
            if not next_worker.available:
                # Already working, consume time
                time = next_worker.remaining
                pool.update_all(time)
            pool.assign_node(next_worker.name, next_node,
                             G.nodes[next_node]['time'])
            pool.nodes_to_consider |= set(G.successors(next_node))
    return pool


add_weight(test_graph, offset=0)
test_pool = walk_graph(test_graph, n_workers=2)
assert test_pool.time_elapsed == 15

add_weight(graph)
pool = walk_graph(graph)
print(f'Solution for part 2: {pool.time_elapsed}')
