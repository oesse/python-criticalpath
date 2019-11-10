import criticalpath

import argparse

parser = argparse.ArgumentParser(
    description='Calculate critical path in a yocto build.'
)
parser.add_argument('depfile', help='dependency graph in graphviz dot format')

args = parser.parse_args()

with open(args.depfile, 'r') as dot_file:
    graph = criticalpath.load_graph_from_dot(dot_file)
    weights = {node: 1 for node in list(graph)}
    critical_path = criticalpath.find_critical_path(graph, weights)

    for node in critical_path:
        print("{node} {weight}".format(node=node, weight=weights[node]))
