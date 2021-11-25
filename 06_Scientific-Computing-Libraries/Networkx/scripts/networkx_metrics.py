"""Helper functions for comparing networks."""

import networkx as nx
import numpy as np


def network_metrics(nx_graph):
    """Returns common network metrics

    Args:
        nx_graph (nx graph): a networkx graph

    Returns:
        dict(
            nb components (int):   number of components
            avg degree (float):    average degree
            avg distance (float):  average distance
            degree distribution (ndarray[int]): degree distribution
        )
    """
    avg_degree = 2 * nx_graph.number_of_edges() / float(nx_graph.number_of_nodes())
    count = 0
    avg_dist = 0
    for component in nx.connected_components(nx_graph):
        subgraph = nx_graph.subgraph(component)
        count += 1
        avg_dist += nx.average_shortest_path_length(subgraph)
    avg_dist /= count
    return {
        "nb components": np.round(count, 2),
        "avg degree": np.round(avg_degree, 2),
        "avg distance": np.round(avg_dist, 2),
        "degree distribution": np.array(nx.degree_histogram(nx_graph)),
    }
