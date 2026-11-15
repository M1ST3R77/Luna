import os
import sys
import platform

def check_executable():
    """
    Check if the executable file for Luna exists.

    :return: 0 if the executable is found, 1 otherwise.
    :rtype: int
    """
    executable_path = ('./executable/luna_windows.exe' if platform.system() == "Windows" else '/app/dist/luna_linux')
    if os.path.exists(executable_path):
        sys.stdout.write(f"{executable_path} found.\n")
        return 0
    else:
        sys.stderr.write(f"{executable_path} not found.\n")
        return 1

if __name__ == "__main__":
    sys.exit(check_executable())