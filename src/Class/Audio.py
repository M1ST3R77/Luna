from espeakng import ESpeakNG
import platform
import pyttsx3
import time

class Audio:
    """
    Manages audio response and its configuration.

    This class handles text-to-speech conversion using different engines 
    depending on the operating system.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the Audio class."""
        self.audio = False
        self.option = "Normal"
        self.voice = "female"
        self.voices = []
        self.rate = 150
        self.volume = 1.0
        self.engine = None

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)
        self.audio = kwargs.get("audio", self.audio)
        self.rate = kwargs.get("rate", self.rate)
        self.volume = kwargs.get("volume", self.volume)
        self.voice = kwargs.get("voice", self.voice)

        if self.audio == True:
            self.init_engine()

        if self.option == "Debug":
            print("[DEBUG] Creating an Audio class variable")

    def init_engine(self):
        """Initializes the TTS engine based on the OS."""
        if platform.system() == "Windows":
            self.engine = pyttsx3.init()
            self.voices = self.get_french_voices()
            self.engine.setProperty('voice', self.voices[1].id if self.voice == "male" else self.voices[0].id)
        else:
            self.engine = ESpeakNG()
            self.engine.voice = "mb-fr3" if self.voice == "male" else "mb-fr4"

    def get_french_voices(self):
        """Fetches French voices, ensuring that 'Hortense' is always at index 0 and 'Paul' at index 1.

        :returns: A list of French voices, with 'Hortense' at index 0 and 'Paul' at index 1 if they exist.
        :rtype: list
        """
        voices = self.engine.getProperty('voices')
        res = []
        tmp = 0

        for v in voices:
            if "French" in v.name:
                if tmp == 0 and "Hortense" in v.name:
                    res.append(v)
                    tmp += 1

        tmp = 0
        for v in voices:
            if "French" in v.name:
                if tmp == 0 and "Paul" in v.name:
                    res.append(v)
                    tmp += 1

        return res    


    def change_voice(self, gender=None):
        """Changes the voice between male and female.

        :param str gender: The desired voice gender ('male' or 'female'). If None, toggles between them.
        :returns: Whether the voice change was successful.
        :rtype: bool
        """
        if not self.engine:
            if self.option == "Debug":
                print("[DEBUG] You haven't activated voice chat")
            return False


        def set_voice(voice_id=None, default_voice=None):
            if platform.system() == "Windows" and voice_id is not None:
                self.engine.setProperty('voice', self.voices[voice_id].id)
            elif default_voice is not None:
                self.engine.voice = default_voice

        if gender:
            self.voice = gender
            if gender == "male":
                set_voice(voice_id=1, default_voice="mb-fr3")
            else:
                set_voice(voice_id=0, default_voice="mb-fr4")
        else:
            if self.voice == "male":
                set_voice(voice_id=0, default_voice="mb-fr4")
                self.voice = "female"
            elif self.voice == "female":
                set_voice(voice_id=1, default_voice="mb-fr3")
                self.voice = "male"
            else:
                set_voice(voice_id=1, default_voice="mb-fr3")
                self.voice = "male"
        
        return True

    def switch_audio(self, audio):
        """Toggles or sets the audio mode.

        :param bool audio: If provided, explicitly sets audio mode.
        """
        if audio == None:
            self.audio = True if self.audio == False else False
        else:
            self.audio = audio

        if self.audio == True:
            self.init_engine()
        else:
            self.engine = None

    def speak(self, text):
        """Speaks the given text if audio is enabled.

        :param str text: The text to be spoken.
        """
        print(text)
        if self.engine == None and self.audio:
            if self.option == "Debug":
                print("[DEBUG] You haven't activated voice chat")
            return

        if self.audio:
            if platform.system() == "Windows":
                self.engine.setProperty('rate', self.rate)
                self.engine.setProperty('volume', self.volume)
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                self.engine.speed= self.rate
                self.engine.volume = int(self.volume * 100)
                self.engine.say(text)
                duration = (len(text.split()) / (self.engine.speed / 60)) / 1.5
                time.sleep(duration)
