.. _Advanced Usage:

Advanced Usage
==============

This section explains how to customize and extend Luna's functionality.

Adding New Responses
--------------------

To add a new response to Luna, modify the **db.json** file located in the **src/files** folder.
For more details, refer to the :ref:`Database <Database>`.

Simple Responses
~~~~~~~~~~~~~~~~

A **simple response** is a basic response that does not trigger any specific action.
Here is an example :

.. code-block:: json

    {
        "tag": "salutations",
        "patterns": ["Salut", "Bonjour", "Coucou", "Hey", "Hello"],
        "responses": ["Salut !", "Bonjour, comment puis-je vous aider ?", "Bonjour, en quoi puis-je être utile aujourd'hui ?", "Hey, ravi de vous voir !"],
        "action": null
    }

To add a simple response, insert a new **JSON object** into the ``intents`` array of **db.json** with ``“action”: null``.

Responses With Actions
~~~~~~~~~~~~~~~~~~~~~~

An **action response** triggers a specific function.
Here is an example :

.. code-block:: json

    {
        "tag": "stop",
        "patterns": ["Arrêt", "Arrête-toi", "Arrête", "toi", "Stop", "Stop-toi"],
        "responses": ["Arrêt de Luna, Bonne journée !"],
        "action": "stop"
    }

To add an action response, create a Python file in the **src/commands** folder with the same name as the ``“action”`` value.
For example, for the ``“stop”`` action, create a **stop.py** file :

.. code-block:: python

    def stop(launch, _):
        launch.stop()

Adding Functional Tests
-----------------------

To add functional tests, create a Python file in the **tests/functional** folder and add a return value, **0** on success and **1** on failure.

Example: Checking Executable Existence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    import sys
    import platform

    def check_executable():
        executable_path = ('./executable/luna_windows.exe' if platform.system() == "Windows" else '/app/dist/luna_linux')
        if os.path.exists(executable_path):
            sys.stdout.write(f"{executable_path} found.\n")
            return 0
        else:
            sys.stderr.write(f"{executable_path} not found.\n")
            return 1

    if __name__ == "__main__":
        sys.exit(check_executable())

Testing Luna's Responses
~~~~~~~~~~~~~~~~~~~~~~~~

To test Luna’s responses to specific phrases, create a text file in **tests/test_files** folder with test phrases.
For example, create a **option.test** file with the following contents :

.. code-block:: text

    hey
    change d'options
    bye
    arrêt

Then use the **return_tester.py** script to check whether the responses are correct :

.. code-block:: python

    from return_tester import return_tester
    import platform
    import sys

    def test_executable_option():
        executable_path = ('./executable/luna_windows.exe' if platform.system() == "Windows" else '/app/dist/luna_linux')
        test_file = './tests/test_files/option.test'

        result = return_tester(executable_path, test_file, True if '-d' in sys.argv else False)
        if result == 0:
            print(f"The executable {executable_path} has successfully changed option.")
            return 0
        else:
            return 1

    if __name__ == "__main__":
        sys.exit(test_executable_option())

Adding Unit Tests
-----------------

To add unit tests, create Python scripts in the **tests/unitaires** folder.

Example: Testing the `Input` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import unittest
    import os
    import sys
    from unittest.mock import patch

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src')))

    from Class.Input import Input
    class TestInput(unittest.TestCase):
        def setUp(self):
            self.input_class = Input("Input")
        
        @patch("builtins.input", return_value="Bonjour")
        def test_input_sentence(self, mock_input):
            res = self.input_class.input_sentence()
            self.assertEqual(res, "Bonjour")
        
        def test_init_default_input(self):
            input_obj = Input("Input")
            self.assertEqual(input_obj.mode, "Input")
            self.assertEqual(input_obj.option, "Normal")
            self.assertEqual(input_obj.language, "fr-FR")
            self.assertEqual(input_obj.silence_threshold, 6)
        
        def test_init_custom_input(self):
            input_obj = Input("Input", "Normal", "en-US", 10)
            self.assertEqual(input_obj.mode, "Input")
            self.assertEqual(input_obj.option, "Normal")
            self.assertEqual(input_obj.language, "en-US")
            self.assertEqual(input_obj.silence_threshold, 10)

    if __name__ == "__main__":
        unittest.main()

All these additions are automatically detected:

- **Database updates** are integrated into Luna’s responses.  
- **Test additions** are automatically included in the test suite.