"""Helper functions for comparing networks."""

import networkx as nx
import numpy as np

"""Helper functions for comparing networks."""

import networkx as nx
import numpy as np


def avg_degree(nx_graph, decimals=None):
    """Return the average node degree of a graph

    Args:
        nx_graph (nx graph): a networkx graph
        decimals (int): number of decimal to round the result

    Returns:
        float: average node degree
    """

    res = 2 * nx_graph.number_of_edges() / nx_graph.number_of_nodes()
    return np.around(res, decimals=decimals) if decimals else res


def degree_distribution(nx_graph):
    """Return the degree distribution of a graph

    Args:
        nx_graph (nx graph): a networkx graph

    Returns:
        ndarray[int]: number of nodes with i edges (i= index)
    """
    return np.array(nx.degree_histogram(nx_graph), dtype=np.int64)


def nb_components(nx_graph):
    """Return the number of components of the graph

    Args:
        nx_graph (nx graph): a networkx graph

    Returns:
        int: number of components
    """
    return len(list(nx.connected_components(nx_graph)))


def avg_distance(nx_graph, decimals=None):
    """Return the average distance of each component of the graph

    Args:
        nx_graph (nx graph): a networkx graph
        decimals (int): number of decimal to round the result

    Returns:
        ndarray[float]: average distance of each component
    """
    lst = [
        nx.average_shortest_path_length(nx_graph.subgraph(subgraph))
        for subgraph in nx.connected_components(nx_graph)
    ]

    # return np.array(lst, dtype=np.float64)
    return np.around(lst, decimals) if decimals else np.array(lst)


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
    return {
        "nb components": nb_components(nx_graph),
        "avg degree": np.round(np.mean(avg_degree(nx_graph)), 2),
        "avg distance": np.round(avg_distance(nx_graph), 4),
        "degree distribution": degree_distribution(nx_graph),
    }


# def network_metrics(nx_graph):
#     """Returns common network metrics

#     Args:
#         nx_graph (nx graph): a networkx graph

#     Returns:
#         dict(
#             nb components (int):   number of components
#             avg degree (float):    average degree
#             avg distance (float):  average distance
#             degree distribution (ndarray[int]): degree distribution
#         )
#     """
#     avg_degree = 2 * nx_graph.number_of_edges() / float(nx_graph.number_of_nodes())
#     count = 0
#     avg_dist = 0
#     for component in nx.connected_components(nx_graph):
#         subgraph = nx_graph.subgraph(component)
#         count += 1
#         avg_dist += nx.average_shortest_path_length(subgraph)
#     avg_dist /= count
#     return {
#         "nb components": np.round(count, 2),
#         "avg degree": np.round(avg_degree, 2),
#         "avg distance": np.round(avg_dist, 2),
#         "degree distribution": np.array(nx.degree_histogram(nx_graph)),
#     }
