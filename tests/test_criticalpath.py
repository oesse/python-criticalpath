import criticalpath


def test_topological_sort_simple_graph():
    graph = {}
    graph[0] = [1]
    graph[1] = []
    assert criticalpath.topological_sort(graph) == [0, 1]


def test_topological_sort_complex_graph():
    graph = {}
    graph[0] = [1, 2]
    graph[1] = [2, 3]
    graph[2] = [3, 4, 5]
    graph[3] = [4, 5]
    graph[4] = [5]
    graph[5] = []

    top_order = criticalpath.topological_sort(graph)

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
