import platform
import sys

if platform.system() == "Windows":
    import msvcrt
elif platform.system() == "Linux":
    import termios
    import tty

class PauseHandler:
    """
    Handles pausing and resuming execution based on user input.

    This class detects key presses to toggle a break option and wait 
    for user input based on the operating system.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the PauseHandler class."""
        self.option = "Normal"
        self.break_opt = False

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        if self.option == "Debug":
            print("[DEBUG] Creating a PauseHandler class variable")

    def break_function(self):
        """
        Toggles the `break_opt` flag.
        """
        self.break_opt = not self.break_opt

    def wait_windows(self):
        """
        Waits for a specific key press on Windows to exit the pause state.

        The monitored key is `0xFD` (corresponding to `²` on an AZERTY keyboard).
        """
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xfd':
                    break

    def wait_linux(self):
        """
        Waits for a specific key press on Linux to exit the pause state.

        The monitored key is `²` on an AZERTY keyboard.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            while True:
                key = sys.stdin.read(1).lower()
                if key == "²":
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def wait_input(self):
        """
        Waits for user input based on the operating system.
        
        Resets `break_opt` to `False` afterward.
        """
        if platform.system() == "Windows":
            self.wait_windows()
        else:
            self.wait_linux()
        self.break_opt = False
