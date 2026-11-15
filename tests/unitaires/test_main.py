import unittest
import sys
from unittest.mock import patch
from main import display_help, run_file_mode, main

class TestMain(unittest.TestCase):
    """
    Unit test suite for the main module.
    """
    @patch("builtins.print")
    def test_display_help(self, mock_print):
        """
        Test the `display_help` function.

        Ensures that the help message is printed correctly.
        """
        display_help()
        mock_print.assert_called_with("  filepath   Launch with a file containing instructions")

    @patch("builtins.print")
    def test_run_file_mode_file_not_found(self, mock_print):
        """
        Test `run_file_mode` when the specified file does not exist.

        Verifies that the function exits with status code 1 and prints an error message.
        """
        with self.assertRaises(SystemExit) as cm:
            run_file_mode("nonexistent_file.txt", debug=False)
        mock_print.assert_called_with("The file 'nonexistent_file.txt' doesn't exist")
        self.assertEqual(cm.exception.code, 1)
    
    @patch("main.display_help")
    def test_main_help_flag(self, mock_display_help):
        """
        Test `main` with the `-h` flag.

        Ensures that the help message is displayed and the function returns 0.
        """
        with patch("sys.argv", ["main.py", "-h"]):
            result = main(sys.argv)
            mock_display_help.assert_called_once()
            self.assertEqual(result, 0)
    
    @patch("main.run_file_mode")
    def test_main_file_mode_bonjour(self, mock_run_file_mode):
        """
        Test `main` when the file `bonjour.test` is provided.

        Ensures that `run_file_mode` is called with the correct file path and debug mode.
        """
        with patch("sys.argv", ["main.py", "tests/test_files/bonjour.test"]):
            main(sys.argv)
            mock_run_file_mode.assert_called_once_with("tests/test_files/bonjour.test", debug=False)
    
    @patch("main.run_file_mode")
    def test_main_file_mode_option(self, mock_run_file_mode):
        """
        Test `main` when the file `option.test` is provided.

        Ensures that `run_file_mode` is called with the correct file path and debug mode.
        """
        with patch("sys.argv", ["main.py", "tests/test_files/option.test"]):
            main(sys.argv)
            mock_run_file_mode.assert_called_once_with("tests/test_files/option.test", debug=False)
    
    @patch("main.run_file_mode")
    def test_main_file_mode_time(self, mock_run_file_mode):
        """
        Test `main` when the file `time.test` is provided.

        Ensures that `run_file_mode` correctly processes the `time.test` file.
        """
        with patch("sys.argv", ["main.py", "tests/test_files/time.test"]):
            main(sys.argv)
            mock_run_file_mode.assert_called_once_with("tests/test_files/time.test", debug=False)
    
    @patch("main.run_file_mode")
    def test_main_file_mode_update(self, mock_run_file_mode):
        """
        Test `main` when the file `update.test` is provided.

        Ensures that `run_file_mode` handles `update.test` properly.
        """
        with patch("sys.argv", ["main.py", "tests/test_files/update.test"]):
            main(sys.argv)
            mock_run_file_mode.assert_called_once_with("tests/test_files/update.test", debug=False)

    @patch("builtins.print")
    def test_main_invalid_option(self, mock_print):
        """
        Test `main` with an invalid option.

        Ensures that an error message is printed and the function returns 1.
        """
        with patch("sys.argv", ["main.py", "-x"]):
            result = main(sys.argv)
            mock_print.assert_called_with("Error: Unknown option '-x', use -h for more information")
            self.assertEqual(result, 1)
    
    @patch("builtins.print")
    def test_main_too_many_arguments(self, mock_print):
        """
        Test `main` with too many arguments.

        Ensures that an error message is printed and the function returns 1.
        """
        with patch("sys.argv", ["main.py", "file1.txt", "file2.txt"]):
            result = main(sys.argv)
            mock_print.assert_called_with("Error: Too many arguments, use -h for more information")
            self.assertEqual(result, 1)
    
if __name__ == "__main__":
    unittest.main()