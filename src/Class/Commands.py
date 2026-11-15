import sys
import os
import importlib
import inspect

class Commands:
    """
    Manages command loading and execution.

    This class dynamically loads all available command functions from Python files
    in the `commands/` directory and allows their execution.

    :param Launch launch_instance: The main code class.
    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, launch_instance, *args, **kwargs):
        """Initializes the Commands class."""
        self.commands = {}
        self.command_folder = os.path.join(sys._MEIPASS, 'commands') if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(__file__), "../commands")
        self.option = "Normal"
        self.launch_instance = launch_instance

        for filename in os.listdir(self.command_folder):
            if filename.endswith(".py"):
                module_name = filename[:-3]
                module_path = f"commands.{module_name}"
                module = importlib.import_module(module_path)
                for name, func in inspect.getmembers(module, inspect.isfunction):
                    self.commands[name] = func
        
        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        if self.option == "Debug":
            print("[DEBUG] Creating a Commands class variable")
    
    def execute(self, command_name, *args, **kwargs):
        """
        Executes a command by name if it exists.

        :param str command_name: The name of the command to execute.
        :param tuple args: Positional arguments passed to the command function.
        :param dict kwargs: Keyword arguments passed to the command function.
        :return: The result of the executed command function, or None if the command is not found.
        :rtype: any
        """
        if command_name in self.commands:
            return self.commands[command_name](self.launch_instance, *args, **kwargs)
        else:
            if self.option == "Debug":
                print(f"[DEBUG] Commande '{command_name}' non trouvée.")
            return None

