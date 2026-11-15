Guide to using and interacting with Luna
========================================

Reminder
--------

Location
~~~~~~~~

As a reminder, the executable:

- **luna_linux** for Linux
- **luna_windows.exe** for Windows

must be located in the *executable* folder

Prerequisites for interaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To launch Luna, you need to install python and these libraries. You can do this by following this tutorial : :ref:`How to install python and its dependencies <Downloads Required User>`

To use Luna's audio functionality, you need to install 2 different voices. You can do this by following this tutorial : :ref:`How to install voices for Luna <Voice Installation>`


For the :ref:`Search` and :ref:`Weather <General Informations>` commands to work properly, you need to configure the following API keys in the `src/files` folder:

1. **Create the `src/files` folder** : If the folder doesn't exist, create it to store your API keys.

2. **OpenWeatherMap API key** :
    - Retrieve your OpenWeatherMap API key from `OpenWeatherMap <https://home.openweathermap.org/api_keys>`_.
    - Create a file named `weather_key` in the `src/files` folder.
    - Copy your API key into this file.

3. **Groq API key** :
    - Retrieve your Groq API key from `Groq Console <https://console.groq.com/keys>`_.
    - Create a file named `groq_key` in the `src/files` folder.
    - Copy your API key into this file.

.. _Documentation Executable:

Usage
-----

Luna can be executed in different ways to suit your needs. Here are the available execution modes :

Normal performance (Voice Recognition)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Command** : ``luna_[linux/windows.exe]``
- **Behavior** : Luna will detect and execute voice commands until you use the :ref:`Stop` interaction.
- **Usage** : Ideal for voice interaction.

Interactive execution with keyboard input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Command** : ``luna_[linux/windows.exe] -i``
- **Behavior** : Luna will wait for you to enter phrases on the keyboard. It will execute the corresponding commands until you use the :ref:`Stop` interaction.
- **Usage** : Handy for testing or using Luna without voice recognition.

Run with a file
~~~~~~~~~~~~~~~

- **Command** : ``luna_[linux/windows.exe] path/to/file.txt``
- **Behavior** : Luna will read the contents of the specified file and execute the sentences it contains. Once the file has been read, the program will stop automatically.
- **Usage** : Useful for automating tasks or testing Luna.

Show Help
~~~~~~~~~

- **Command** : ``luna_[linux/windows.exe] -h``
- **Behavior** : Displays usage options and available execution modes.
- **Usage** : Useful for reminding you of the different ways to launch the program.

Debug Mode
~~~~~~~~~~
- **Flag**: ``luna_[linux/windows.exe] -d``
- **Behavior**: Provides debug information throughout the program execution.
- **Usage**: Can be combined with other flags for detailed debugging.

Graphical User Interface
~~~~~~~~~~~~~~~~~~~~~~~~
- **Flag**: ``luna_[linux/windows.exe] -w``
- **Behavior**: Launches Luna's graphical user interface.
- **Usage**: Provides a visual interface for interacting with Luna.

.. note::
   - The **debug flag** (-d) can be combined with other flags for more detailed output.
   - The **graphical interface** (-w) does not support :ref:`Break <Break>` command, switching to :ref:`Input <Interaction>` mode, and does not handle :ref:`Audio <Audio>` on Windows.