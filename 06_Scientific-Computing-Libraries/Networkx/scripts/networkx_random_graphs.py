"""Helper functions to generate various random graph given an expected average degree."""

import networkx as nx
import numpy as np


def avg_degree_to_erdos_renyi_kwargs(nb_nodes, avg_degree):
    """Convert parameters to usable inputs for networkx.erdos_renyi_graph()

    Args:
        nb_nodes (int):     number of nodes
        avg_degree (float): expected average degree of the graph

    Returns:
        dict(          keyword arguments
            n (int):   number of nodes
            p (float): edge probability (in [0,1])
        )
    """
    edge_probability = avg_degree / nb_nodes
    return {"n": nb_nodes, "p": edge_probability}


def avg_degree_to_watts_strogatz_kwargs(nb_nodes, avg_degree, rewiring_probability):
    """Convert parameters to usable inputs for networkx.watts_strogatz_graph()

    Args:
        nb_nodes (int):               number of nodes
        avg_degree (float):           expected average degree of the graph
        rewiring_probability (float): rewiring probability (in [0,1])

    Returns:
        dict(          keyword arguments
            n (int):   number of nodes
            k (int):   initial number of neighbors
            p (float): rewiring probability (in [0,1])
        )
    """
    nb_neighbours = round(avg_degree)
    return {"n": nb_nodes, "k": nb_neighbours, "p": rewiring_probability}


def avg_degree_to_barabasi_albert_kwargs(nb_nodes, avg_degree):
    """Convert parameters to usable inputs for networkx.barabasi_albert_graph()

    Args:
        nb_nodes (int):     number of nodes
        avg_degree (float): expected average degree of the graph

    Returns:
        dict(          keyword arguments
            n (int):   number of nodes
            m (int):   initial clique
        )
    """
    if not compatible_barabasi_albert_params(nb_nodes, avg_degree):
        raise ValueError(
            f"barabasi_albert_graph():"
            f"expected average degree ({avg_degree}) is too low"
            f"compared to the number of nodes ({nb_nodes})."
        )
    nb_neighbours = get_barabasi_albert_m_arg_from_avg_degree(nb_nodes, avg_degree)
    return {"n": nb_nodes, "m": nb_neighbours}


def compatible_barabasi_albert_params(nb_nodes, avg_degree):
    """Check if necessary conditions are met for generating a Barabasi Albert graph.
    See annex (end of notebook) for more details about the explanation.

    Args:
        nb_nodes (int):             number of nodes
        avg_degree (float):  expected average degree of the graph

    Returns:
        bool: valid parameters
    """
    return avg_degree <= nb_nodes ** 2 / (2 * (nb_nodes + 1))


def get_barabasi_albert_m_arg_from_avg_degree(nb_nodes, avg_degree):
    """Generate the initial clique value (m) inputs for networkx.barabasi_albert_graph().
    See annex (end of notebook) for more details about the explanation.

    Args:
        n (int):            number of nodes
        avg_degree (float): expected average degree of the graph

    Returns:
        int:   initial clique (m)
    """
    return round(
        np.min(np.roots([2 / (nb_nodes + 1), 2 / (nb_nodes + 1) - 2, avg_degree]))
    )


def generate_random_graph(network_type, nb_nodes, avg_degree):
    """Generate a random graph

    Args:
        network_type (string): type of random graph (erdos_renyi / watts_strogatz / barabasi_albert)
        nb_nodes (int): number of nodes
        avg_degree (int/float): expected average degree

    Returns:
        networkx.classes.graph.Graph: a networkx graph
    """
    graph = {
        "random": {
            "generator": nx.erdos_renyi_graph,
            "param": avg_degree_to_erdos_renyi_kwargs(nb_nodes, avg_degree),
        },
        "small world": {
            "generator": nx.watts_strogatz_graph,
            "param": avg_degree_to_watts_strogatz_kwargs(nb_nodes, avg_degree, 0.5),
        },
        "scale free": {
            "generator": nx.barabasi_albert_graph,
            "param": avg_degree_to_barabasi_albert_kwargs(nb_nodes, avg_degree),
        },
    }
    return graph[network_type]["generator"](**graph[network_type]["param"])
