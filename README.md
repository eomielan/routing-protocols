# Routing Protocols

## Overview

This project is a Python implementation of the link state and distance vector routing protocols. There are two separate programs: one that implements the link state protocol, and one that implements the distance vector protocol. Both programs read and use the same file format for the network’s topology as well as the same format for messages to send.

The documentation for this project was generated using Doxygen and can be found by opening `doxygen/html/index.html` in a browser. If there are any issues viewing the documentation, follow these steps to generate it locally:

1. Install [Doxygen](https://www.doxygen.nl/).
2. In the command line, navigate to the doxygen directory using `cd doxygen`.
3. Next, run `doxygen Doxyfile` to generate the documentation.
4. The documentation can be viewed by opening the file `doxygen/html/index.html` in a browser.

## Instructions

1. Run `chmod +x dvr.sh lsr.sh setup.sh` once before running the programs.
2. Run `python3 -m venv myenv` and then `source myenv/bin/activate` to start a virtual environment.
3. Run `./setup.sh` in the virtual environment to install dependencies.

    **NOTE:** If you encounter the following error when running `./setup.sh`:

    ```
    ./setup.sh: line 2: $'\r': command not found
    ./setup.sh: line 20: syntax error: unexpected end of file
    ```

    First run `dos2unix setup.sh` to convert the line endings in `setup.sh` to Unix-style line endings, then run `./setup.sh` again.

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
    
    **NOTE:** The tests require dos2unix to run on Linux. If you do not already have this package installed please run the following:

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
