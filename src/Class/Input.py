import speech_recognition as sr

class Input:
    """
    Handles user input through speech recognition or manual text input.

    This class allows switching between voice and text input modes, configuring recognition settings, 
    and capturing user input with optional debug information.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    :param str option: Debug mode ('Normal' or 'Debug'). Defaults to 'Normal'.
    :param str input: Predefined input (used only in text mode). Defaults to None.
    :param str language: Language code for speech recognition (e.g., 'fr-FR'). Defaults to 'fr-FR'.
    :param int silence_threshold: Energy threshold for detecting speech. Defaults to 6.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the Input class."""
        self.mode = "Vocal"
        self.option = "Normal"
        self.input = None
        self.language = "fr-FR"
        self.silence_threshold = 6
        self.recognizer = None

        if len(args) == 0:
            self.recognizer = sr.Recognizer()
        elif len(args) == 1 and args[0] == "Input":
            self.mode = "Input"
        elif len(args) == 1 and args[0] == "Vocal":
            self.recognizer = sr.Recognizer()
        elif len(args) == 3:
            self.mode, self.option, self.input = args
        elif len(args) == 4:
            self.mode, self.option, self.language, self.silence_threshold = args
            self.recognizer = sr.Recognizer()
        
        self.mode = kwargs.get("mode", self.mode)
        self.option = kwargs.get("option" or "opt", self.option)
        self.input = kwargs.get("input", self.input)
        self.language = kwargs.get("language", self.language)
        self.silence_threshold = kwargs.get("sensibility", self.silence_threshold)
        if self.mode == "Vocal" and not self.recognizer:
            self.recognizer = sr.Recognizer()

        if self.option == "Debug":
            print("[DEBUG] Creating an Input class variable")

    def input_sentence(self, opt="base"):
        """
        Captures user input either through voice recognition or manual input.

        :param str opt: Mode for text prompt ('base' for default prompt, anything else for silent mode).
        :return: Recognized text if detected, None otherwise.
        :rtype: str or None
        """
        if self.mode != "Vocal":
            return input("Entrez votre phrase :\n" if opt == "base" else "")

        try:
            with sr.Microphone() as mic:
                print("Écoute...\n" if opt == "base" else "", end="")
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic)

                if self.recognizer.energy_threshold < self.silence_threshold:
                    if self.option == "Debug":
                        print("[DEBUG] No significant sound detected.")
                    return None

                text = self.recognizer.recognize_google(audio, language=self.language)
                text = text.lower()

                if self.option == "Debug":
                    print("[DEBUG] Here's what you said: " + text)
                return text

        except:
            print("Aucune phrase n'a été détectée\n" if opt == "base" else "", end="")
            return None