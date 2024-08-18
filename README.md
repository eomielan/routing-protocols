# Routing Protocols

## Overview

This project is a Python implementation of the link state and distance vector routing protocols. There are two separate programs: one that implements the link state protocol, and one that implements the distance vector protocol. Both programs read and use the same file format for the network’s topology as well as the same format for messages to send.

## Instructions

1. Run `chmod +x dvr.sh lsr.sh setup.sh` to make the scripts executable.
2. Run `python3 -m venv myenv` and then `source myenv/bin/activate` to start a virtual environment.
3. Run `pip install -r requirements.txt` in the virtual environment to install dependencies.
4. To start a simulation, run one of the following commands:

    #### Distance Vector Routing Protocol

    ```
    ./dvr.sh <topologyFile> <messageFile> <changesFile> [outputFile]
    ```

    Example:

    ```
    ./dvr.sh topology.txt message.txt changes.txt
    ```

    #### Link State Routing Protocol:

    ```
    ./lsr.sh <topologyFile> <messageFile> <changesFile> [outputFile]
    ```

    Example:

    ```
    ./lsr.sh topology.txt message.txt changes.txt
    ```

5. Run `pytest` to run the tests.
    
    **NOTE:** The tests require `dos2unix` to run on Linux. If you do not already have this package installed please run:

    ```bash
    sudo apt-get update
    sudo apt-get install dos2unix
    ```

6. Run `deactivate` to stop the virtual environment.

## Testing

We used [Pytest](https://docs.pytest.org/en/8.0.x/), a Python testing framework, to test our code. These test files can be found in the `src/test` directory.

To run the test suite:

1. Ensure you have Pytest installed.
2. In the command line, run `pytest` to start the test suite.

Note that you can run the test suite from the root or `src/test` directory. The root directory rely on the bash scripts to run, while running the tests from `src/test` do not require the bash scripts.
