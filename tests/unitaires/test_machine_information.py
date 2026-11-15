import unittest
import tempfile
from utils.machine_information import (
    generate_acronym,
    list_exec_desktop
)

class TestUtils(unittest.TestCase):
    """Unit tests for utility functions."""

    def test_generate_acronym(self):
        """Test acronym generation from executable names."""
        self.assertEqual(generate_acronym("Visual Studio Code"), "VSC")
        self.assertEqual(generate_acronym("firefox"), "F")
        self.assertEqual(generate_acronym("My_Application_v2"), "MAV")
        self.assertEqual(generate_acronym(""), "")

    def test_list_exec_desktop_no_executables(self):
        """Test case where no executables are found on desktop."""
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(list_exec_desktop(temp_dir), ["Erreur : Aucun exécutable trouvé sur le Bureau"])

    def test_list_exec_desktop_invalid_path(self):
        """Test handling of invalid desktop path."""
        self.assertEqual(list_exec_desktop("non_existent_path"), ["Erreur : Impossible d'accéder au Bureau"])

if __name__ == "__main__":
    unittest.main()
