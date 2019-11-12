import criticalpath

import argparse

parser = argparse.ArgumentParser(
    prog='criticalpath',
    description='Calculate critical path in a yocto build.'
)
parser.add_argument('depfile', help='dependency graph in graphviz dot format')
parser.add_argument('stats_dirs', nargs='+',
                    help='one or more buildstats directories')
parser.add_argument('-t', '--target', help='find critical path up to target')
parser.add_argument('-s', '--source', help='find critical path from source')
parser.add_argument('--missing', action='store_true',
                    help='print steps for which no stats could be found')


def main(args):
    graph = load_graph(args.depfile)
    weights = load_weights(args.stats_dirs, graph)

    if args.missing:
        print_missing_stats(graph, weights)
        return

    critical_path = criticalpath.find_critical_path(graph,
                                                    weights,
                                                    args.source,
                                                    args.target)

    for node in critical_path:
        print("{node} {weight}".format(node=node, weight=weights[node]))


def load_graph(filename):
    with open(filename, 'r') as dot_file:
        return criticalpath.load_graph_from_dot(dot_file)


def load_weights(stats_dirs, graph):
    cache = criticalpath.BuildstatsCache(stats_dirs)
    return {node: cache.load_elapsed_time(node) for node in list(graph)}


def print_missing_stats(graph, weights):
    missing_stats = [node for node in list(graph)
                     if weights[node] == 0]
    for node in missing_stats:
        print(node)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
