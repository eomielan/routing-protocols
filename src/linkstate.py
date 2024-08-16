"""A link state routing implementation."""

import sys
from pathlib import Path
from typing import IO, List, Tuple

from ls_graph import LSGraph, create_LSGraph


def compute_forwarding_table(graph: LSGraph, source_node: int) -> List[Tuple[int, int, int]]:
    """Compute the forwarding table for a given source node.

    Args:
        graph (LSGraph): The link state graph.
        source_node (int): The source node for which to compute the forwarding table.

    Returns:
        List[Tuple[int, int, int]]: A list of tuples, where each tuple contains the destination
            node, the next hop, and the path cost.
    """
    forwarding_table = []

    shortest_paths = {}
    for node in graph.get_nodes():
        shortest_paths[node] = graph.dijkstra_shortest_path(source_node, node)

    sorted_destinations = sorted(shortest_paths.keys())

    for dest in sorted_destinations:
        # Ignore unreachable nodes
        if shortest_paths[dest]:
            next_hop = shortest_paths[dest][1] if dest != source_node else source_node
            path_cost = graph.calculate_path_cost(shortest_paths[dest])
            forwarding_table.append((dest, next_hop, path_cost))

    return forwarding_table


def write_forwarding_tables(graph: LSGraph, output_file: IO[str]) -> None:
    """This function writes the forwarding tables for all nodes in a link state graph to an output
    file. Each entry is separated by a new line. The format for each entry in the forwarding table
    is as follows:
    ```
    <destination> <next_hop> <path_cost>
    ```

    Args:
        graph (LSGraph): The link state graph.
        output_file (IO[str]): The output file to write the forwarding tables to.
    """
    for node_id in sorted(graph.get_nodes()):
        forwarding_table = compute_forwarding_table(graph, node_id)
        for entry in forwarding_table:
            output_file.write(f"{entry[0]} {entry[1]} {entry[2]}\n")
        output_file.write("\n")


def write_messages(graph: LSGraph, msg_file: IO[str], output_file: IO[str]) -> None:
    """This function writes the messages from a message file to an output file. For each message,
    it determines the least cost path from the source to destination node and writes the message
    along with the path and path cost to the output file.

    If the destination node is reachable from the source node, the output will be formatted as:
    ```
    from <src_id> to <dest_id> cost <pathCost> hops <hop1> <hop2> <...> message <message>
    ```

    If the destination node is unreachable from the source node, the output will be formatted as:
    ```
    from <src_id> to <dest_id> cost infinite hops unreachable message <message>
    ```

    Args:
        graph (LSGraph): The link state graph.
        msg_file (IO[str]): The message file to read the messages from.
        output_file (IO[str]): The output file to write the messages to.
    """
    msg_file.seek(0)
    for line in msg_file:
        parts = line.strip().split()
        if len(parts) >= 4:
            source, dest, message = parts[0], parts[1], " ".join(parts[2:])
            path = graph.dijkstra_shortest_path(int(source), int(dest))
            path_cost = graph.calculate_path_cost(path)
            if path_cost != -1 and path:
                output_file.write(
                    f"from {source} to {dest} cost {path_cost} hops "
                    f"{' '.join(map(str, path[:-1]))} message {message}\n"
                )
            else:
                output_file.write(
                    f"from {source} to {dest} cost infinite hops unreachable message {message}\n"
                )
        else:
            output_file.write(
                f"from {parts[0]} to {parts[1]} cost infinite hops unreachable message <message>\n"
            )
        output_file.write("\n")


def main() -> int:
    """This function is the entrypoint of the program. It parses the command line arguments and
    calls the appropriate functions to start the simulation.

    The arguments passed in must follow the form:
    ```
    <topologyFile> <messageFile> <changesFile> [outputFile]
    ```

    Returns:
        int: 0 if the program executed successfully, an error code otherwise.
    """
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <topologyFile> <messageFile> <changesFile> [outputFile]")
        return 1

    topology_file = Path(sys.argv[1])
    message_file = Path(sys.argv[2])
    changes_file = Path(sys.argv[3])
    output_file = Path(sys.argv[4]) if len(sys.argv) >= 5 else Path("output.txt")

    try:
        with open(topology_file) as topo_file, open(message_file) as msg_file, open(
            changes_file
        ) as chg_file, open(output_file, "w") as out_file:
            graph = create_LSGraph(topo_file)

            write_forwarding_tables(graph, out_file)
            write_messages(graph, msg_file, out_file)

            for line in chg_file:
                line = line.strip()
                if not line:
                    continue

                id1, id2, cost = map(int, line.split())

                # IF node does not exist, add it
                if id1 not in graph.get_nodes():
                    graph.add_node(id1)
                if id2 not in graph.get_nodes():
                    graph.add_node(id2)

                # If edge does not exist, add it
                if not graph._graph.has_edge(id1, id2) and not graph._graph.has_edge(id2, id1):
                    graph.add_edge(id1, id2, cost)

                # Otherwise, update the cost of the edge
                elif cost != -999:
                    graph.change_cost(id1, id2, cost)
                else:
                    graph.remove_edge(id1, id2)

                write_forwarding_tables(graph, out_file)
                write_messages(graph, msg_file, out_file)
    except OSError:
        print("Error opening files")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
