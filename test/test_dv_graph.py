"""Tests for the distance vector graph implementation."""

import os
import platform
import subprocess

import pytest

from src.dv_graph import create_DVGraph


def test_neighbours_added():
    current_dir = os.getcwd()

    if os.path.basename(current_dir) == "test":
        topology_file = "files/topology.txt"
    else:
        topology_file = os.path.join("test/files", "topology.txt")

    with open(topology_file) as topology_file:
        graph = create_DVGraph(topology_file)

    assert sorted(graph.nodes.keys()) == [1, 2, 3, 4, 5]

    assert graph.get_node(1).neighbors[4] == 1
    assert graph.get_node(1).neighbors[2] == 8
    assert graph.get_node(1).distance_vector[4][1] == 1
    assert graph.get_node(1).distance_vector[2][1] == 6

    assert graph.get_node(2).neighbors[1] == 8
    assert graph.get_node(2).neighbors[3] == 3
    assert graph.get_node(2).neighbors[5] == 4
    assert graph.get_node(2).distance_vector[1][1] == 6
    assert graph.get_node(2).distance_vector[3][1] == 3
    assert graph.get_node(2).distance_vector[5][1] == 4

    assert graph.get_node(3).neighbors[2] == 3
    assert graph.get_node(3).distance_vector[2][1] == 3

    assert graph.get_node(4).neighbors[1] == 1
    assert graph.get_node(4).neighbors[5] == 1
    assert graph.get_node(4).distance_vector[1][1] == 1
    assert graph.get_node(4).distance_vector[5][1] == 1

    assert graph.get_node(5).neighbors[2] == 4
    assert graph.get_node(5).neighbors[4] == 1
    assert graph.get_node(5).distance_vector[2][1] == 4
    assert graph.get_node(5).distance_vector[4][1] == 1


def test_paths_to_other_nodes():
    current_dir = os.getcwd()

    if os.path.basename(current_dir) == "test":
        topology_file = "files/topology.txt"
    else:
        topology_file = os.path.join("test/files", "topology.txt")

    with open(topology_file) as topology_file:
        graph = create_DVGraph(topology_file)

    assert graph.get_node(1).distance_vector[2][1] == 6
    assert graph.get_node(1).distance_vector[3][1] == 9
    assert graph.get_node(1).distance_vector[4][1] == 1
    assert graph.get_node(1).distance_vector[5][1] == 2

    assert graph.get_node(2).distance_vector[1][1] == 6
    assert graph.get_node(2).distance_vector[3][1] == 3
    assert graph.get_node(2).distance_vector[4][1] == 5
    assert graph.get_node(2).distance_vector[5][1] == 4

    assert graph.get_node(3).distance_vector[1][1] == 9
    assert graph.get_node(3).distance_vector[2][1] == 3
    assert graph.get_node(3).distance_vector[4][1] == 8
    assert graph.get_node(3).distance_vector[5][1] == 7

    assert graph.get_node(4).distance_vector[1][1] == 1
    assert graph.get_node(4).distance_vector[2][1] == 5
    assert graph.get_node(4).distance_vector[3][1] == 8
    assert graph.get_node(4).distance_vector[5][1] == 1

    assert graph.get_node(5).distance_vector[1][1] == 2
    assert graph.get_node(5).distance_vector[2][1] == 4
    assert graph.get_node(5).distance_vector[3][1] == 7
    assert graph.get_node(5).distance_vector[4][1] == 1

    assert graph.get_node(1).distance_vector[3][0] == [1, 4, 5, 2, 3]
    assert graph.get_node(1).distance_vector[4][0] == [1, 4]
    assert graph.get_node(1).distance_vector[5][0] == [1, 4, 5]

    assert graph.get_node(2).distance_vector[5][0] == [2, 5]

    assert graph.get_node(4).distance_vector[3][0] == [4, 5, 2, 3]
    assert graph.get_node(4).distance_vector[5][0] == [4, 5]


@pytest.mark.parametrize(
    "graph_type, message_file, changes_file, expected_output_file",
    [
        ("dvr.sh", "message.txt", "changes.txt", "expected_output.txt"),
        ("dvr.sh", "unlink_message.txt", "unlink_changes.txt", "unlink_expected_output.txt"),
        ("dvr.sh", "new_edge_message.txt", "new_edge_changes.txt", "new_edge_expected_output.txt"),
        ("dvr.sh", "empty.txt", "empty.txt", "empty_expected_output.txt"),
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
        dvr_process = subprocess.Popen(
            [
                "python3",
                "../src/distancevector.py",
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
        dvr_process = subprocess.Popen(
            [f"./{graph_type}", topology_file, message_file, changes_file, output_file]
        )

    dvr_process.wait()

    with open(expected_output_file) as expected_output_file:
        expected_output = expected_output_file.read()

    with open(output_file) as output_file:
        output = output_file.read()

    assert output.strip() == expected_output.strip()


if __name__ == "__main__":
    pytest.main(["-v"])
