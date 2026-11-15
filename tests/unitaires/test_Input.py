import unittest
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src')))

from Class.Input import Input
class TestInput(unittest.TestCase):
    """
    Unit tests for the `Input` class.
    """
    def setUp(self):
        """
        Set up an `Input` instance before each test case.
        """
        self.input_class = Input("Input")
    
    @patch("builtins.input", return_value="Bonjour")
    def test_input_sentence(self, mock_input):
        """
        Test the `input_sentence` method.

        Simulates user input and verifies that the method correctly returns the input value.
        """
        res = self.input_class.input_sentence()
        self.assertEqual(res, "Bonjour")
    
    def test_init_default_input(self):
        """
        Test the default initialization of the `Input` class.

        Ensures that the default values for mode, option, language, and silence threshold are correctly set.
        """
        input_obj = Input("Input")
        self.assertEqual(input_obj.mode, "Input")
        self.assertEqual(input_obj.option, "Normal")
        self.assertEqual(input_obj.language, "fr-FR")
        self.assertEqual(input_obj.silence_threshold, 6)
    
    def test_init_custom_input(self):
        """
        Test the initialization of the `Input` class with custom parameters.

        Verifies that provided values override the default ones.
        """
        input_obj = Input("Input", "Normal", "en-US", 10)
        self.assertEqual(input_obj.mode, "Input")
        self.assertEqual(input_obj.option, "Normal")
        self.assertEqual(input_obj.language, "en-US")
        self.assertEqual(input_obj.silence_threshold, 10)

if __name__ == "__main__":
    unittest.main()