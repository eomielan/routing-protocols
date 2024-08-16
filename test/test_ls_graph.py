"""Tests for the link state graph implementation."""

import os
import platform
import subprocess

import pytest

from src.ls_graph import create_LSGraph


def test_create_graph_from_topology_file():
    current_dir = os.getcwd()

    if os.path.basename(current_dir) == "test":
        topology_file = "files/topology.txt"
    else:
        topology_file = os.path.join("test/files", "topology.txt")

    with open(topology_file) as topology_file:
        graph = create_LSGraph(topology_file)

    assert graph._graph.has_node(1)
    assert graph._graph.has_node(2)
    assert graph._graph.has_node(3)
    assert graph._graph.has_node(4)
    assert graph._graph.has_node(5)

    assert graph._graph.has_edge(1, 2)
    assert graph._graph.has_edge(2, 1)

    edge_data = graph._graph.get_edge_data(1, 2)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 8
    edge_data = graph._graph.get_edge_data(2, 1)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 8

    assert graph._graph.has_edge(2, 3)
    assert graph._graph.has_edge(3, 2)

    edge_data = graph._graph.get_edge_data(2, 3)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 3
    edge_data = graph._graph.get_edge_data(3, 2)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 3

    assert graph._graph.has_edge(2, 5)
    assert graph._graph.has_edge(5, 2)

    edge_data = graph._graph.get_edge_data(2, 5)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 4
    edge_data = graph._graph.get_edge_data(5, 2)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 4

    assert graph._graph.has_edge(4, 1)
    assert graph._graph.has_edge(1, 4)

    edge_data = graph._graph.get_edge_data(4, 1)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 1
    edge_data = graph._graph.get_edge_data(1, 4)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 1

    assert graph._graph.has_edge(4, 5)
    assert graph._graph.has_edge(5, 4)

    edge_data = graph._graph.get_edge_data(4, 5)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 1
    edge_data = graph._graph.get_edge_data(5, 4)
    assert edge_data is not None and "weight" in edge_data
    assert edge_data["weight"] == 1


def test_dijkstra_shortest_path():
    current_dir = os.getcwd()

    if os.path.basename(current_dir) == "test":
        topology_file = "files/topology.txt"
    else:
        topology_file = os.path.join("test/files", "topology.txt")

    with open(topology_file) as topology_file:
        graph = create_LSGraph(topology_file)

    path = graph.dijkstra_shortest_path(1, 3)
    assert path == [1, 4, 5, 2, 3]

    path = graph.dijkstra_shortest_path(1, 5)
    assert path == [1, 4, 5]

    path = graph.dijkstra_shortest_path(2, 5)
    assert path == [2, 5]

    path = graph.dijkstra_shortest_path(4, 3)
    assert path == [4, 5, 2, 3]

    path = graph.dijkstra_shortest_path(4, 5)
    assert path == [4, 5]


@pytest.mark.parametrize(
    "graph_type, message_file, changes_file, expected_output_file",
    [
        ("lsr.sh", "message.txt", "changes.txt", "expected_output.txt"),
        ("lsr.sh", "unlink_message.txt", "unlink_changes.txt", "unlink_expected_output.txt"),
        ("lsr.sh", "new_edge_message.txt", "new_edge_changes.txt", "new_edge_expected_output.txt"),
        ("lsr.sh", "empty.txt", "empty.txt", "empty_expected_output.txt"),
    ],
)
def test_graph_behaviour(graph_type, message_file, changes_file, expected_output_file):
    current_dir = os.getcwd()
    os_name = platform.system()

    if os.path.basename(current_dir) == "test":
        topology_file = "files/topology.txt"
        message_file = f"files/{message_file}"
        changes_file = f"files/{changes_file}"
        output_file = "../output.txt"
        expected_output_file = f"files/{expected_output_file}"
        if os_name == "Windows" or os_name == "Linux":
            subprocess.run(["dos2unix", f"../{graph_type}"])
        lsr_process = subprocess.Popen(
            [
                "python3",
                "../src/linkstate.py",
                topology_file,
                message_file,
                changes_file,
                output_file,
            ]
        )
    else:
        topology_file = os.path.join("test/files", "topology.txt")
        message_file = os.path.join("test/files", message_file)
        changes_file = os.path.join("test/files", changes_file)
        output_file = "output.txt"
        expected_output_file = os.path.join("test/files", expected_output_file)
        if os_name == "Windows" or os_name == "Linux":
            subprocess.run(["dos2unix", f"./{graph_type}"])
        lsr_process = subprocess.Popen(
            [f"./{graph_type}", topology_file, message_file, changes_file, output_file]
        )

    lsr_process.wait()

    with open(expected_output_file) as expected_output_file:
        expected_output = expected_output_file.read()

    with open(output_file) as output_file:
        output = output_file.read()

    assert output.strip() == expected_output.strip()


if __name__ == "__main__":
    pytest.main(["-v"])
