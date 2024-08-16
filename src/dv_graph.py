"""A distance vector graph implementation."""

from typing import IO, Dict, Set


class Node:
    """This class represents a node within a Distance Vector graph. Each node contains a unique
    identifier, a list of its neighbors, and a distance vector that contains the shortest path to
    each destination node.

    Attributes:
        id (int): The unique identifier for the node.
        neighbors (dict): A dictionary of the node's neighbors, where the key is the neighbor's
            ID and the value is the cost to reach the neighbor.
        distance_vector (dict): A dictionary of the shortest path to each destination node, where
            the key is the destination node's ID and the value is a tuple containing the path and
            the cost to reach the destination.
    """

    def __init__(self, id: int):
        self.id = id
        self.neighbors: Dict[int, int] = {}
        self.distance_vector = {id: ([id], 0)}


class DVGraph:
    """This class is used to represent a Distance Vector Graph. The graph is composed of nodes
    that are connected by edges. Each node contains a unique identifier, a list of its neighbors,
    and a distance vector that contains the shortest path to each destination node.

    Attributes:
        nodes (dict): A dictionary of the nodes in the graph, where the key is the node's ID and
            the value is the Node object.
    """

    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id: int) -> bool:
        """Add a node to the graph.

        Args:
            node_id (int): The unique identifier for the node.

        Returns:
            bool: True if the node was added successfully, False if the node already exists.
        """
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = Node(node_id)
        return True

    def get_node(self, node_id: int) -> Node:
        """Get a node from the graph.

        Args:
            node_id (int): The unique identifier for the node. This must correspond to the ID of a
                node within the graph, otherwise a KeyError will be raised.

        Returns:
            Node: The node with the specified ID.
        """
        return self.nodes[node_id]

    def add_edge(self, node_id1: int, node_id2: int, cost: int) -> bool:
        """This function adds an edge to the graph between two nodes, with the specified cost. If
        either of the nodes does not exist within the graph, the edge will not be added. The change
        will be propagated to all nodes connected to either node of the edge.

        Args:
            node_id1 (int): The unique identifier for the first node.
            node_id2 (int): The unique identifier for the second node.
            cost (int): The cost of the edge between the two nodes.

        Returns:
            bool: True, if the edge was added successfully, and False otherwise.
        """
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False

        node1 = self.nodes[node_id1]
        node2 = self.nodes[node_id2]

        node1.neighbors[node_id2] = cost
        node2.neighbors[node_id1] = cost

        self.propagate_change(node_id1)
        self.propagate_change(node_id2)

        return True

    def change_cost(self, node_id1: int, node_id2: int, new_cost: int) -> bool:
        """This function changes the cost of an edge between two nodes. If either of the nodes does
        not exist within the graph, no changes are made. The change will be propagated to all nodes
        connected to either node of the edge.

        Args:
            node_id1 (int): The unique identifier for the first node.
            node_id2 (int): The unique identifier for the second node.
            new_cost (int): The new cost of the edge between the two nodes.

        Returns:
            bool: True, if the cost was changed successfully, and False otherwise.
        """
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False

        if (
            node_id2 not in self.nodes[node_id1].neighbors
            or node_id1 not in self.nodes[node_id2].neighbors
        ):
            return False

        return self.add_edge(node_id1, node_id2, new_cost)

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """This function removes an edge from the graph between two nodes. If either of the nodes
        does not exist within the graph, no changes are made. If the nodes with the edge to remove
        are not already neighbors, no changes are made.

        Otherwise, the edge between the specified nodes is removed, and the change is propagated to
        all nodes connected to either node of the edge. Note that any path containing the removed
        edge is invalidated.

        Args:
            node_id1 (int): The unique identifier for the first node.
            node_id2 (int): The unique identifier for the second node.

        Returns:
            bool: True, if the edge was removed successfully, and False otherwise.
        """
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False

        if (
            node_id2 not in self.nodes[node_id1].neighbors
            or node_id1 not in self.nodes[node_id2].neighbors
        ):
            return False

        node1 = self.nodes[node_id1]
        node2 = self.nodes[node_id2]

        node1.neighbors.pop(node_id2)
        node2.neighbors.pop(node_id1)

        node1.distance_vector.pop(node_id2)
        node2.distance_vector.pop(node_id1)

        # Invalidate any path containing the removed edge
        for node_id in self.nodes:
            node = self.get_node(node_id)

            for dest_id, (path, cost) in list(node.distance_vector.items()):
                for i in range(len(path) - 1):
                    if (path[i], path[i + 1]) == (node_id1, node_id2) or (
                        path[i],
                        path[i + 1],
                    ) == (node_id2, node_id1):
                        node.distance_vector.pop(dest_id)
                        break

        self.propagate_change(node_id1)
        self.propagate_change(node_id2)

        return True

    def construct_connected_nodes_queue(self, source_id: int) -> Set[int]:
        """This function traverses the source node's distance vector table to create a set of nodes
        connected to it. If a node is not within the source node's distance vector table, it is
        considered not connected and will not be included in the set, even if the node exists
        within the overall Distance Vector graph.

        Args:
            source_id (int): The unique identifier for the source node.

        Returns:
            Set[int]: A set of all node IDs connected to the source node.
        """
        queue = [source_id]
        visited = set(queue)

        while queue:
            current_id = queue.pop(0)
            current_node = self.nodes[current_id]

            for neighbor_id in current_node.neighbors:
                if neighbor_id not in visited:
                    queue.append(neighbor_id)
                    visited.add(neighbor_id)

        return visited

    def propagate_change(self, source_id: int) -> None:
        """This function propagates a change in the graph to all nodes connected to the source
        node. The change is propagated by first traversing through the source node's neighbors,
        then the neighbors of the neighbors, and so on. Note that the change is only propagated to
        nodes that are connected to the source node. Other nodes will not be affected by the
        change, even if they exist within the overall Distance Vector graph.

        - If the new path has a lower cost, the distance vector of the neighbor node is updated.
        - If the new path has the same cost, the path with the lowest node ID prior to the
          destination node is chosen. If both paths have the same node ID prior to the destination
          node, the previous node is checked until the tie is broken.

        Args:
            source_id (int): The unique identifier for the source node.
        """
        # Create a queue of all nodes connected to the source node
        queue = list(self.construct_connected_nodes_queue(source_id))

        while queue:
            current_id = queue.pop(0)
            current_node = self.nodes[current_id]

            # Check each neighbor of the current node
            for neighbor_id, cost_to_neighbor in current_node.neighbors.items():
                neighbor_node = self.nodes[neighbor_id]

                # Calculate the potential new cost from current node to this neighbor
                for dest_id, (path, cost) in current_node.distance_vector.items():
                    if neighbor_id == dest_id:
                        continue  # Skip if the neighbor is the destination itself

                    new_cost = cost + cost_to_neighbor
                    new_path = [neighbor_id] + path

                    # Update if this new path is better than the previously known path
                    if (
                        dest_id not in neighbor_node.distance_vector
                        or new_cost < neighbor_node.distance_vector[dest_id][1]
                    ):
                        neighbor_node.distance_vector[dest_id] = (new_path, new_cost)
                        queue.append(neighbor_id)

                    # If the new path has the same cost, choose the path with the lowest node ID
                    # prior to the destination node
                    elif (
                        new_cost == neighbor_node.distance_vector[dest_id][1]
                        and new_path != neighbor_node.distance_vector[dest_id][0]
                    ):
                        tie_broken = False
                        best_path = None

                        while not tie_broken:
                            i = -2

                            existing_path = neighbor_node.distance_vector[dest_id][0]

                            if existing_path[i] < new_path[i]:
                                tie_broken = True
                                best_path = existing_path

                            elif existing_path[i] > new_path[i]:
                                tie_broken = True
                                best_path = new_path

                            else:
                                i -= 1

                        neighbor_node.distance_vector[dest_id] = (best_path, new_cost)
                        queue.append(neighbor_id)


def create_DVGraph(topology_file: IO[str]) -> DVGraph:
    """Create a Distance Vector Graph object from a topology file.

    Args:
        topology_file (IO[str]): topology_file The file containing the topology of the network.

    Returns:
        DVGraph: The Distance Vector Graph created from the topology file.
    """
    graph = DVGraph()

    # Initialize each node in the graph and add edges
    for line in topology_file:
        line = line.strip()
        if not line:
            continue

        id1, id2, cost = map(int, line.split())
        if graph.add_node(id1):
            graph.add_node(id1)
        if graph.add_node(id2):
            graph.add_node(id2)

        graph.add_edge(id1, id2, cost)

    return graph
