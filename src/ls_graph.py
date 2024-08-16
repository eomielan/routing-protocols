"""A link state graph implementation."""

from typing import IO, List

import networkx as nx


class LSGraph:
    """A class representing a Link State Graph.

    Attributes:
        _graph (nx.Graph): A NetworkX graph object representing the link state graph.
    """

    def __init__(self):
        self._graph = nx.Graph()

    def add_node(self, n: int) -> bool:
        """Add a node to the graph.

        Args:
            n (int): The node to add.

        Returns:
            bool: True, if the node was added successfully, and False, if the node was not added
                (i.e. it already exists in the graph).
        """
        if n in self._graph:
            return False
        self._graph.add_node(n)
        return True

    def get_nodes(self) -> List[int]:
        """Get the nodes in the graph.

        Returns:
            List[int]: A list of the nodes in the graph.
        """
        return list(self._graph.nodes)

    def add_edge(self, n1: int, n2: int, cost: int) -> bool:
        """Add an edge to the graph.

        Args:
            n1 (int): The node that the edge starts at.
            n2 (int): The node that the edge ends at.
            cost (int): The cost of the edge.

        Returns:
            bool: True, if the edge was added successfully, and False, if the edge was not added
                (i.e. it already exists in the graph or the nodes it connects do not exist).
        """
        if not self._graph.has_node(n1) or not self._graph.has_node(n2):
            return False

        if self._graph.has_edge(n1, n2):
            return False

        self._graph.add_edge(n1, n2, weight=cost)
        return True

    def change_cost(self, n1: int, n2: int, newCost: int) -> bool:
        """Change the cost of an edge between two nodes.

        Args:
            n1 (int): The first node of the edge.
            n2 (int): The second node of the edge.
            newCost (int): The new cost of the edge.

        Returns:
            bool: True, if the cost was changed successfully, and False, if the edge does not exist
                in the graph.
        """
        if self._graph.has_edge(n1, n2):
            self._graph[n1][n2]["weight"] = newCost
            return True
        return False

    def remove_edge(self, n1: int, n2: int) -> bool:
        """Remove an edge from the graph.

        Args:
            n1 (int): The first node of the edge.
            n2 (int): The second node of the edge.

        Returns:
            bool: True, if the edge was removed successfully, and False, if the edge does not exist
                in the graph.
        """
        if self._graph.has_edge(n1, n2):
            self._graph.remove_edge(n1, n2)
            return True
        return False

    def calculate_path_cost(self, path: List[int]) -> int:
        """Calculate the cost of a path.

        Args:
            path (List[int]): The path to calculate the cost of.

        Returns:
            int: The cost of the path, and -1 if the path is empty.
        """
        if not path:
            return -1

        total_cost = sum(self._graph[path[i]][path[i + 1]]["weight"] for i in range(len(path) - 1))
        return total_cost

    def dijkstra_shortest_path(self, source: int, dest: int) -> List[int]:
        """Get the shortest path between two nodes using Dijkstra's algorithm.

        Args:
            source (int): The starting node.
            dest (int): The ending node.

        Returns:
            List[int]: The shortest path between the two nodes, or an empty list if no path
                exists. If multiple shortest paths exist, the path with the lowest node ID prior to
                the destination node is returned. If there is a tie, the algorithm keeps checking
                the previous node until the tie is broken.
        """
        try:
            paths = list(nx.all_shortest_paths(self._graph, source, dest, weight="weight"))

            if len(paths) == 1:
                return paths[0]
            else:
                min_node_id = float("inf")
                min_path = []
                tie_broken = False

                i = -2

                while not tie_broken:
                    for p in paths:
                        if p[i] < min_node_id:
                            min_node_id = p[i]
                            min_path = p
                            tie_broken = True
                        elif p[i] == min_node_id:
                            i -= 1
                            min_node_id = float("inf")
                            tie_broken = False
                            break

            return min_path

        except nx.NetworkXNoPath:
            return []


def create_LSGraph(topology_file: IO[str]) -> LSGraph:
    """Create a Link State Graph object from a topology file.

    Args:
        topology_file (IO[str]): The file containing the topology of the network.

    Returns:
        LSGraph: The graph created from the topology file.
    """
    graph = LSGraph()

    for line in topology_file:
        line = line.strip()
        if not line:
            continue

        id1, id2, cost = map(int, line.split())

        graph.add_node(id1)
        graph.add_node(id2)
        graph.add_edge(id1, id2, cost)

    return graph
