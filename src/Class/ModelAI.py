import os

os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, GRU
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Input, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import tensorflow as tf
import numpy as np

class ModelAI:
    """
    Manages the AI model for text classification.

    This class handles the creation, training, and loading of a deep learning 
    model using TensorFlow's Keras.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the ModelAI class."""
        self.option = "Normal"
        self.model_file = 'src/files/AI.keras'
        self.model = None

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        if self.option == "Debug":
            print("[DEBUG] Creating a ModelAI class variable")

    def training(self, db_train_x, db_train_y):
        """
        Trains the AI model on the given dataset.

        The model is a recurrent neural network (RNN) with LSTM layers. It is 
        trained using categorical cross-entropy loss and the Adam optimizer.

        :param np.ndarray db_train_x: Input training data of shape (samples, features).
        :param np.ndarray db_train_y: Corresponding output labels in one-hot encoding.
        """
        db_train_x = np.expand_dims(db_train_x, axis=1)

        self.model = Sequential()
        self.model.add(Input(shape=(db_train_x.shape[1], db_train_x.shape[2])))

        self.model.add(LSTM(256, return_sequences=True, activation='swish', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.5))

        self.model.add(GRU(128, return_sequences=True, activation='swish', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.5))

        self.model.add(LSTM(64, return_sequences=False, activation='swish', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.5))

        self.model.add(Dense(len(db_train_y[0]), activation='softmax', kernel_regularizer=tf.keras.regularizers.l2(0.01)))

        optimizer = RMSprop(learning_rate=0.001, momentum=0.9)
        self.model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['accuracy'])
        checkpoint = ModelCheckpoint(self.model_file, monitor='loss', save_best_only=True, verbose=0)
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-6, verbose=0)
        self.model.fit(db_train_x, db_train_y, epochs=600, batch_size=16, verbose=0, callbacks=[checkpoint, reduce_lr])
        if self.option == "Debug":
            print(f"[DEBUG] Model saved as '{self.model_file}'.")

    def get_model_ai(self):
        """
        Loads and returns the trained AI model.

        :return: The trained TensorFlow Keras model.
        :rtype: Sequential
        """
        return tf.keras.models.load_model(self.model_file)