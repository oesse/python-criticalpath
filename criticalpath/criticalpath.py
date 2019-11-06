def add_edge(graph, source, target):
    """Add an edge from source to target in the graph"""
    if source not in graph:
        graph[source] = []
    if target not in graph:
        graph[target] = []

    graph[source].append(target)


def topological_sort(graph):
    """Return a topologically sorted list of all nodes in the graph"""
    from collections import deque

    in_degree = _count_incoming_edges(graph)
    node_queue = deque([node for node, degree in in_degree.items()
                        if degree == 0])

    top_order = []
    while len(node_queue) != 0:
        node = node_queue.popleft()
        top_order.append(node)

        for adjacent_node in graph[node]:
            in_degree[adjacent_node] -= 1
            if in_degree[adjacent_node] == 0:
                node_queue.append(adjacent_node)

    return top_order


def _count_incoming_edges(graph):
    in_degree = {node: 0 for node in list(graph)}

    for node, adjacent_nodes in graph.items():
        for adjacent_node in adjacent_nodes:
            in_degree[adjacent_node] += 1

    return in_degree


def find_critical_path(in_graph, weights):
    """Return the critical path through the graph considering given weights"""
    import copy
    graph = copy.deepcopy(in_graph)

    virtual_sink = _add_virtual_sink(graph)

    top_order = topological_sort(graph)
    roots = _take_roots(top_order, graph)

    distances = {node: (0 if node in roots else float('-inf'))
                 for node in list(graph)}
    predecessor_nodes = {node: i for i, node in enumerate(list(graph))}

    for node in top_order:
        for adjacent_node in graph[node]:
            d = distances[node] + weights.get(node, 0)
            if distances[adjacent_node] < d:
                distances[adjacent_node] = d
                predecessor_nodes[adjacent_node] = node

    return _construct_path(predecessor_nodes, virtual_sink)


def _add_virtual_sink(graph):
    sinks = [node for node, adjacent_nodes in graph.items()
             if len(adjacent_nodes) == 0]

    virtual_sink = _unique_key(graph)
    for sink in sinks:
        add_edge(graph, sink, virtual_sink)

    return virtual_sink


def _unique_key(graph):
    import random
    import string

    return ''.join(random.sample(string.ascii_letters, 5))


def _take_roots(top_order, graph):
    seen_nodes = set()
    roots = []
    for node in top_order:
        if node in seen_nodes:
            break

        for adjacent_node in graph[node]:
            seen_nodes.add(adjacent_node)

        roots.append(node)
    return roots


def _construct_path(predecessor_nodes, target_node):
    current_node = predecessor_nodes[target_node]
    print(predecessor_nodes)
    path = [current_node]
    while True:
        predecessor = predecessor_nodes[current_node]
        if predecessor == current_node:
            break
        path.append(predecessor)
        current_node = predecessor

    path.reverse()
    return path
