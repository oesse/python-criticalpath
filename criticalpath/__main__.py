import criticalpath

import argparse

parser = argparse.ArgumentParser(
    prog='criticalpath',
    description='Calculate critical path in a yocto build.'
)
parser.add_argument('depfile', help='dependency graph in graphviz dot format')


def main(depfile):
    graph = load_graph(depfile)
    weights = {node: 1 for node in list(graph)}
    critical_path = criticalpath.find_critical_path(graph, weights)

    for node in critical_path:
        print("{node} {weight}".format(node=node, weight=weights[node]))


def load_graph(filename):
    with open(filename, 'r') as dot_file:
        return criticalpath.load_graph_from_dot(dot_file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.depfile)
