import nltk
import pickle
import numpy as np

class ChatBot:
    """
    Manages user input processing, intent prediction, and response generation.

    This class loads a trained model, tokenizes user input, predicts the intent, 
    and selects an appropriate response based on predefined intents.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the ChatBot class."""
        self.option = "Normal"
        self.model = None
        self.words = None
        self.classes = None
        self.data = None

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        if self.option == "Debug":
            print("[DEBUG] Creating a ChatBot class variable")

    def loading(self, model, data):
        """Loads the chatbot model and training data.

        :param model: The trained model for intent classification.
        :param dict data: The dictionary containing intents and responses.
        """
        self.model = model
        self.data = data
        self.words = pickle.load(open('src/files/words.pkl', 'rb'))
        self.classes = pickle.load(open('src/files/classes.pkl', 'rb'))

    def preprocess_input(self, sentence):
        """Tokenizes and converts a sentence into a bag-of-words representation.

        :param str sentence: The input sentence to process.
        :returns: A NumPy array representing the bag-of-words.
        :rtype: numpy.ndarray
        """
        words = nltk.word_tokenize(sentence)
        bag = [1 if word in words else 0 for word in self.words]

        return np.array(bag).reshape(1, 1, len(bag))

    def predict_class(self, sentence):
        """Predicts the intent of a given sentence based on the trained model.

        :param str sentence: The user input sentence.
        :returns: A list of intents with their respective probabilities.
        :rtype: list[dict[str, str]]
        """
        bow = self.preprocess_input(sentence)
        res = self.model.predict(bow, verbose=0)[0]
        threshold = 0.35
        results = [[i, r] for i, r in enumerate(res) if r > threshold]

        if self.option == "Debug":
            np.set_printoptions(suppress=True, precision=4)
            formatted_res = ", ".join(map(str, res))
            print(f"[DEBUG] Here are the probabilities for all categories: {formatted_res}")
        results.sort(key=lambda x: x[1], reverse=True)
        return [{"intent": self.classes[r[0]], "probability": str(r[1])} for r in results]

    def get_response(self, launch, sentence, audio):
        """Generates a response based on the predicted intent of the input sentence.

        :param Launch launch: The main code class.
        :param str sentence: The user input sentence to be processed.
        :param Audio audio: The class handling audio responses.
        """
        if sentence == None:
            return
        intents = self.predict_class(sentence)
        if self.option == "Debug":
            print(f"[DEBUG] Here is the result: {intents}")
        if intents:
            tag = intents[0]['intent']
            for intent in self.data['intents']:
                if intent['tag'] == tag:
                    action = intent.get("action")
                    response = np.random.choice(intent['responses'])
                    audio.speak(response)
                    if action:
                        launch.commands.execute(action, sentence)
                    return

        for intent in self.data['intents']:
            if intent['tag'] == "non_reconnu":
                audio.speak(np.random.choice(intent['responses']))
                return