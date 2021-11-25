import networkx as nx
import numpy as np


def network_metrics(G):
    """Returns common network metrics

    Args:
        G (nx graph): a networkx graph

    Returns:
        dict(
            nb components (int):   number of components
            avg degree (float):    average degree
            avg distance (float):  average distance
            degree distribution (ndarray[int]): degree distribution
        )
    """
    avg_degree = 2 * G.number_of_edges() / float(G.number_of_nodes())
    count = 0
    avg_dist = 0
    for component in nx.connected_components(G):
        g = G.subgraph(component)
        count += 1
        avg_dist += nx.average_shortest_path_length(g)
    avg_dist /= count
    return {
        "nb components": np.round(count, 2),
        "avg degree": np.round(avg_degree, 2),
        "avg distance": np.round(avg_dist, 2),
        "degree distribution": np.array(nx.degree_histogram(G)),
    }


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
    if not is_valid_BA_params(nb_nodes, avg_degree):
        raise ValueError(
            f"barabasi_albert_graph():"
            f"expected average degree ({avg_degree}) is too low"
            f"compared to the number of nodes ({nb_nodes})."
        )
    nb_neighbours = BA_initial_clique_from_avg_degree(nb_nodes, avg_degree)
    return {"n": nb_nodes, "m": nb_neighbours}


def is_valid_BA_params(n, avg_degree):
    """Check if necessary conditions are met for generating a Barabasi Albert graph.
    See annex (end of notebook) for more details about the explanation.

    Args:
        n (int):             number of nodes
        avg_degree (float):  expected average degree of the graph

    Returns:
        bool: valid parameters
    """
    return avg_degree <= n ** 2 / (2 * (n + 1))


def BA_initial_clique_from_avg_degree(n, avg_degree):
    """Generate the initial clique value (m) inputs for networkx.barabasi_albert_graph().
    See annex (end of notebook) for more details about the explanation.

    Args:
        n (int):            number of nodes
        avg_degree (float): expected average degree of the graph

    Returns:
        int:   initial clique (m)
    """
    return round(np.min(np.roots([2 / (n + 1), 2 / (n + 1) - 2, avg_degree])))


def generate_random_graph(network_type, nb_nodes, avg_degree):
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
