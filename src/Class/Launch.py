from .Input import Input
from .Database import Database
from .ModelAI import ModelAI
from .ChatBot import ChatBot
from .Commands import Commands
from .Detector import Detector
from .Audio import Audio
from .PauseHandler import PauseHandler
import os

class Launch:
    """
    Manages the initialization and execution of all components.

    This class serves as the central controller, managing interactions between
    the input system, database, AI model, chatbot, detector, audio response, 
    pause handler, and command execution.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the Launch class."""
        self.input = Input(*args, **kwargs)
        self.db = Database(*args, **kwargs)
        self.ai = ModelAI(*args, **kwargs)
        self.chatbot = ChatBot(*args, **kwargs)
        self.detector = Detector(*args, **kwargs)
        self.audio = Audio(*args, **kwargs)
        self.pausehandler = PauseHandler(*args, **kwargs)
        self.commands = Commands(self, *args, **kwargs)
        self.option = "Normal"
        self.running = True

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        self.loading()

        if self.option == "Debug":
            print("[DEBUG] Creating a Launch class variable")

    def update(self):
        """
        Updates the AI model and database.

        This function preprocesses the database, retrains the AI model, and reloads
        the chatbot's configuration.
        """
        self.db.preprocess()
        self.ai.training(self.db.train_x, self.db.train_y)
        self.loading()

    def loading(self):
        """
        Loads or updates the chatbot model based on database changes.

        If necessary files are missing or the database has been modified, it triggers an update.
        Otherwise, it loads the chatbot with the latest AI model and intents.
        """
        if not os.path.exists(self.db.words_file) or not os.path.exists(self.db.classes_file) or not os.path.exists(self.ai.model_file):
            self.update()
        elif self.detector.has_db_file_changed():
            if self.option == "Debug":
                print("[DEBUG] The Database has been modified, update launched")
            self.update()
        self.chatbot.loading(self.ai.get_model_ai(), self.db.load_intents())

    def switch_opt(self, opt):
        """
        Toggles or sets the operation mode of all components.

        If `opt` is None, it switches between 'Normal' and 'Debug' mode.
        Otherwise, it explicitly sets all components to the given mode.

        :param str opt: The operation mode ('Normal' or 'Debug'). Defaults to None.
        """
        for obj in [self.input, self.db, self.chatbot, self.ai, self.detector, self.commands, self.audio, self]:
            if opt == None:
                obj.option = "Debug" if obj.option == "Normal" else "Normal"
            else:
                obj.option = opt

    def switch_mode(self):
        """
        Toggles the input mode between 'Vocal' and 'Input'.
        """
        self.input.mode = "Vocal" if self.input.mode == "Input" else "Input"

    def stop(self):
        """
        Stops the execution loop by setting `running` to False.
        """
        self.running = False