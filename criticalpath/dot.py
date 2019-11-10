from .criticalpath import add_edge
import re


class ParseError(Exception):
    pass


def load_graph_from_dot(dot_stream):
    """Read dot_stream and parse the content into a graph dictionary"""

    lines = dot_stream.readlines()
    first_line = lines[0]
    if not re.match(r'^digraph\s+(\w+)\s+{$', first_line):
        raise ParseError("expected digraph header")

    edge_pattern = re.compile(r'^"([^"]*)"\s+->\s+"([^"]*)"$')
    node_pattern = re.compile(r'^"([^"]*)"\s+\[[^\]]*\]$')
    graph = {}
    for line in lines[1:-1]:
        match = edge_pattern.match(line)
        if match:
            source_node, target_node = match.groups()
            add_edge(graph, source_node, target_node)
        elif not node_pattern.match(line):
            raise ParseError("expected edge or node statement")

    if lines[-1] != "}":
        raise ParseError("expected '}'")

    return graph
