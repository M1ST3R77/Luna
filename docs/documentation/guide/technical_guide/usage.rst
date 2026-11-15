Guide to launch Luna and its various features
=============================================

Usage
-----

Luna can be launched in two different ways: 

- By building it with **Pymake**
- By running **main.py** with **Python**

.. _Documentation Pymake:

Build
~~~~~

Requirements for build Luna
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build Luna, you'll need to install docker if you're on Linux, and python and its libraries. You can do this by following this tutorial : :ref:`How to install docker, python and its dependencies <Downloads Required Technical>`

Pymake
^^^^^^

Pymake can be executed in different ways to suit your needs. Here are the available execution modes :

Build the program and create executable
.......................................

- **Command** : ``python pymake`` (Windows) or ``./pymake`` (Linux)
- **Behavior** : Builds the program and creates the executable for your operating system, `luna_linux` (Linux) or `luna_windows` (Windows).
- **Usage** : Use this when you want to create or update the Luna executable.

Clean build artifacts
.....................

- **Command** : ``python pymake clean`` (Windows) or ``./pymake clean`` (Linux)
- **Behavior** : Removes Docker container (Linux) or build folder with .spec files (Windows).
- **Usage** : Use this to clean up after a build.

Full clean
..........

- **Command** : ``python pymake fclean`` (Windows) or ``./pymake fclean`` (Linux)
- **Behavior** : Removes Docker container, image, volume (Linux) and executable (Linux and Windows).
- **Usage** : Use this for a complete cleanup of all build artifacts.

Rebuild
.......

- **Command** : ``python pymake re`` (Windows) or ``./pymake re`` (Linux)
- **Behavior** : Launches a full clean and a build.
- **Usage** : Use this to ensure a fresh build from scratch.

Run tests
.........

- **Command** : ``python pymake tests`` (Windows) or ``./pymake tests`` (Linux)
- **Behavior** : Launches functional and unit tests to ensure that Luna works properly, creates a test results report and a coverage HTML page.
- **Usage** : Use this to verify the functionality of Luna.

View test coverage
..................

- **Command** : ``python pymake coverage`` (Windows) or ``./pymake coverage`` (Linux)
- **Behavior** : Opens the HTML coverage report in your default browser.
- **Usage** : Use this to analyze the test coverage of Luna.

Update documentation
....................

- **Command** : ``python pymake doc_auto`` (Windows) or ``./pymake doc_auto`` (Linux)
- **Behavior** : Updates documentation and creates the documentation page.
- **Usage** : Use this when you've made changes and need to update the documentation.

View documentation
..................

- **Command** : ``python pymake doc`` (Windows) or ``./pymake doc`` (Linux)
- **Behavior** : Opens the documentation page in your default browser.
- **Usage** : Use this to read the Luna documentation.

Debug mode
..........

- **Flag** : ``-d``
- **Behavior** : Enables debug mode to see all messages during execution.
- **Usage** : Add this flag to any command for verbose output.

Show Help
.........

- **Command** : ``python pymake -h/--help/-help`` (Windows) or ``./pymake -h/--help/-help`` (Linux)
- **Behavior** : Displays usage options and available execution modes.
- **Usage** : Use this to remind yourself of the different ways to use pymake.

Note: Pymake works only on Windows and Linux operating systems. The behavior may differ slightly between these platforms, particularly for build and clean operations.

Run from Code
~~~~~~~~~~~~~

Prerequisites
^^^^^^^^^^^^^

To run the program from code, you'll need to have Python installed and the required dependencies. You can do this by following this tutorial : :ref:`Install the necessary dependencies to launch from code<Downloads Required Technical To Launch From Code>`

Virtual environment (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's highly recommended to use a virtual environment to isolate the project dependencies.

At the root of the project, run the commands

1. **Create a virtual environment**

    .. code-block:: bash

        python3 -m venv venv

2. **Activate the virtual environment**

    - On Linux :
    
        .. code-block:: bash

            source venv/bin/activate
    
    - On Windows :

        .. code-block:: powershell

            .\venv\Scripts\activate


Install dependencies
^^^^^^^^^^^^^^^^^^^^

Run the following command to install the required python dependencies :

    .. code-block:: bash

        pip install -r docker/requirements.txt

Running the program
^^^^^^^^^^^^^^^^^^^

Once the python dependencies have been downloaded, you can run the program :

    .. code-block:: bash

        python src/main.py