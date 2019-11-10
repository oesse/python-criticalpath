from criticalpath import load_graph_from_dot
import io


def test_load_empty_graph():
    dot_stream = io.StringIO("""digraph depends {
}""")
    graph = load_graph_from_dot(dot_stream)

    assert graph == {}


def test_load_graph_with_single_edge():
    dot_stream = io.StringIO("""digraph depends {
"source.node" -> "target.node"
}""")
    graph = load_graph_from_dot(dot_stream)

    expected = {
        "source.node": ["target.node"],
        "target.node": [],
    }
    assert graph == expected


def test_load_graph_with_multiple_edges():
    dot_stream = io.StringIO("""digraph depends {
"a.node" -> "b.node"
"a.node" -> "c.node"
"b.node" -> "c.node"
}""")
    graph = load_graph_from_dot(dot_stream)

    expected = {
        "a.node": ["b.node", "c.node"],
        "b.node": ["c.node"],
        "c.node": [],
    }
    assert graph == expected


def test_load_graph_with_node_statement():
    dot_stream = io.StringIO("""digraph depends {
"a.node" [label="some label"]
"a.node" -> "b.node"
}""")
    graph = load_graph_from_dot(dot_stream)

    expected = {
        "a.node": ["b.node"],
        "b.node": [],
    }
    assert graph == expected
