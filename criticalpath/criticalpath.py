def topological_sort(graph):
    """Returns a topologically sorted list of all nodes in the graph"""

    in_degree = _count_incoming_edges(graph)
    node_queue = [node for node, degree in in_degree.items()
                  if degree == 0]

    top_order = []
    while len(node_queue) != 0:
        node = node_queue.pop(0)
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
