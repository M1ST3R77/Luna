from nltk.stem import WordNetLemmatizer
import numpy as np
import nltk
import pickle
import os
import json
import ssl

class Database:
    """
    Handles database operations for chatbot training data.

    This class manages the loading, processing, and saving of words, classes,
    and intent data used for training a chatbot model.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the Database class."""
        self.option = "Normal"
        self.words_file = 'src/files/words.pkl'
        self.classes_file = 'src/files/classes.pkl'
        self.intents_file = 'src/db.json'
        self.train_x = []
        self.train_y = []
        self.lemmatizer = WordNetLemmatizer()

        ssl._create_default_https_context = ssl._create_unverified_context
        nltk.download('punkt', quiet=True)
        nltk.download("punkt_tab", quiet=True)
        nltk.download('wordnet', quiet=True)

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        if self.option == "Debug":
            print("[DEBUG] Creating a Database class variable")

    def save_objects(self, words, classes):
        """
        Saves words and classes objects as pickle files.
        
        :param list words: List of processed words.
        :param list classes: List of intent classes.
        """
        pickle.dump(words, open(self.words_file, 'wb'))
        pickle.dump(classes, open(self.classes_file, 'wb'))
    
    def load_intents(self):
        """
        Loads intents from a JSON file.
        
        :returns: Parsed JSON content.
        :rtype: dict
        """
        with open(self.intents_file, encoding='utf-8') as file:
            return json.load(file)

    def preprocess(self):
        """
        Performs preprocessing on intent data.
        """
        os.makedirs("src/files", exist_ok=True)
        intents = self.load_intents()
        words, classes = self.preprocess_data(intents)
        self.save_objects(words, classes)
        if self.option == "Debug":
            print("[DEBUG] Pre-processing complete and objects saved.")

    def preprocess_data(self, intents):
        """
        Tokenizes and lemmatizes words from the intent dataset.
        
        :param dict intents: Dictionary containing chatbot intents.
        :returns: Processed words and classes.
        :rtype: tuple[list, list]
        """
        words = set()
        classes = set()
        documents = []
        ignore_words = ['?', '!']

        for intent in intents['intents']:
            tag = intent['tag']
            for pattern in intent['patterns']:
                word_list = [self.lemmatizer.lemmatize(w.lower()) for w in nltk.word_tokenize(pattern) if w not in ignore_words]
                words.update(word_list)
                documents.append((word_list, tag))
                classes.add(tag)

        words = sorted(words)
        classes = sorted(classes)

        training = [
            (
                [1 if word in word_list else 0 for word in words],
                [1 if cls == tag else 0 for cls in classes]
            )
            for word_list, tag in documents
        ]

        np.random.shuffle(training)
        self.train_x = np.array([t[0] for t in training])
        self.train_y = np.array([t[1] for t in training])

        return words, classes

