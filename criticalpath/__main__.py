import criticalpath

import argparse

parser = argparse.ArgumentParser(
    prog='criticalpath',
    description='Calculate critical path in a yocto build.'
)
parser.add_argument('depfile', help='dependency graph in graphviz dot format')
parser.add_argument('stats_dirs', nargs='+',
                    help='one or more buildstats directories')


def main(depfile, stats_dirs):
    graph = load_graph(depfile)
    weights = load_weights(stats_dirs, graph)
    critical_path = criticalpath.find_critical_path(graph, weights)

    for node in critical_path:
        print("{node} {weight}".format(node=node, weight=weights[node]))


def load_graph(filename):
    with open(filename, 'r') as dot_file:
        return criticalpath.load_graph_from_dot(dot_file)


def load_weights(stats_dirs, graph):
    cache = criticalpath.BuildstatsCache(stats_dirs)
    return {node: cache.load_elapsed_time(node) for node in list(graph)}


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.depfile, args.stats_dirs)
