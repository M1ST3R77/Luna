from return_tester import return_tester
import platform
import sys

def test_executable_update():
    """
    Test if the executable correctly handles updates.

    :return: 0 if the test passes, 1 otherwise.
    :rtype: int
    """
    executable_path = ('./executable/luna_windows.exe' if platform.system() == "Windows" else '/app/dist/luna_linux')
    test_file = './tests/test_files/update.test'

    result = return_tester(executable_path, test_file, True if '-d' in sys.argv else False)
    if result == 0:
        print(f"The executable {executable_path} updated successfully.")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(test_executable_update())
