.. _Architecture:

Architecture
============

Pymake
------

**Pymake** is a Python-based build system similar to a Makefile. It serves as the central tool for building the executable and includes additional functionalities such as running tests.
For more details, refer to the :ref:`Pymake documentation <Documentation Pymake>`.

github/workflows
----------------

This directory contains configuration files for **GitHub Actions**, enabling automated testing and deployment.

docker
------

This directory contains all files required to manage the **Docker environment** :

- **Dockerfile** : Defines the Docker environment for building the executable.
- **requirements.txt** : Lists the Python dependencies needed to run Luna.

docs
----

documentation
~~~~~~~~~~~~~

This directory contains all the technical tools for building documentation, as well as the content of project documentation.

reports
~~~~~~~

coverage
^^^^^^^^

Contains an HTML report of the test coverage along with its configuration.

test_reports
^^^^^^^^^^^^

Stores all reports generated after running the tests.

executable
----------

This directory holds the generated **Luna executable**.
For more details, refer to the :ref:`Executable documentation <Documentation Executable>`.

tests
-----

- **run_tests.py** : Main script to execute all tests.

test_files
~~~~~~~~~~

Contains files used for functional tests.

functional
~~~~~~~~~~

Contains functional test scripts.

unitaires
~~~~~~~~~

Contains unit test scripts.

src
---

This directory contains all **Luna source files**.

- **db.json** : A database file storing all possible Luna responses.

Class
~~~~~

Contains all Luna classes.

commands
~~~~~~~~

Scripts related to Luna's commands and responses.

files
~~~~~

API key files and files needed to build the AI.

utils
~~~~~

Utility scripts for reusable functions.