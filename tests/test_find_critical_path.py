from criticalpath import add_edge, find_critical_path


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