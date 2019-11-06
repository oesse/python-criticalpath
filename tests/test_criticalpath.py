from criticalpath import add_edge, find_critical_path, topological_sort


def test_topological_sort_simple_graph():
    graph = {}
    add_edge(graph, 0, 1)
    assert topological_sort(graph) == [0, 1]


def test_topological_sort_complex_graph():
    graph = {}
    add_edge(graph, 0, 1)
    add_edge(graph, 0, 2)
    add_edge(graph, 1, 2)
    add_edge(graph, 1, 3)
    add_edge(graph, 2, 3)
    add_edge(graph, 2, 4)
    add_edge(graph, 2, 5)
    add_edge(graph, 3, 4)
    add_edge(graph, 3, 5)
    add_edge(graph, 4, 5)

    top_order = topological_sort(graph)

    assert top_order.index(0) < top_order.index(1)
    assert top_order.index(0) < top_order.index(2)

    assert top_order.index(1) < top_order.index(3)
    assert top_order.index(1) < top_order.index(2)

    assert top_order.index(2) < top_order.index(4)
    assert top_order.index(2) < top_order.index(5)
    assert top_order.index(2) < top_order.index(3)

    assert top_order.index(3) < top_order.index(5)
    assert top_order.index(3) < top_order.index(4)

    assert top_order.index(4) < top_order.index(5)


def test_find_critical_path_simple_graph():
    graph = {}
    add_edge(graph, 0, 1)
    add_edge(graph, 0, 2)
    add_edge(graph, 1, 3)
    add_edge(graph, 2, 3)
    weights = {0: 1,
               1: 2,
               2: 1,
               3: 1}

    assert find_critical_path(graph, weights) == [0, 1, 3]


def test_find_critical_path_missing_weights_are_ignored():
    graph = {}
    add_edge(graph, 0, 1)
    add_edge(graph, 0, 2)
    add_edge(graph, 1, 3)
    add_edge(graph, 2, 3)
    weights = {0: 1,
               # weight for 1 is missing
               2: 1,
               3: 1}

    assert find_critical_path(graph, weights) == [0, 2, 3]
