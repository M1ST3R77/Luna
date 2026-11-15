from Class.Launch import Launch
from Class.Widget import Widget
from PyQt5.QtWidgets import QApplication
import sys
import sounddevice

def display_help():
    """
    Display the usage information for the program.
    """
    print("Usage: luna_[linux/windows.exe] [-h] [-d] [filepath]")
    print("Description: ")
    print("  -h         Display usage")
    print("  -i         Launch in input mode")
    print("  -d         Launch in debug mode")
    print("  -w         Launch in widget mode")
    print("  filepath   Launch with a file containing instructions")


def run_file_mode(file, debug=False):
    """
    Execute Luna using a file containing predefined instructions.

    :param str file: The path to the file containing instructions.
    :param bool debug: Whether to run in debug mode, defaults to False.
    """
    launch = Launch(mode="Input", option="Debug" if debug else "Normal")
    try:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    launch.chatbot.get_response(launch, line, launch.audio)
    except FileNotFoundError:
        print(f"The file '{file}' doesn't exist")
        sys.exit(1)


def run_mode(mode="Vocal", debug=False):
    """
    Execute Luna in either vocal or input mode.

    :param str mode: The mode to run the assistant in ("Vocal" or "Input"), defaults to "Vocal".
    :param bool debug: Whether to run in debug mode, defaults to False.
    """
    launch = Launch(mode=mode, option="Debug" if debug else "Normal")
    while launch.running:
        if launch.pausehandler.break_opt:
            launch.pausehandler.wait_input()
            launch.audio.speak("Luna est de nouveau opérationnelle !")
        sentence = launch.input.input_sentence()
        launch.chatbot.get_response(launch, sentence, launch.audio)


def run_widget_mode(debug=False):
    """
    Launch Luna in widget mode.
    """
    app = QApplication(sys.argv)
    window = Widget(debug)
    window.show()
    sys.exit(app.exec_())


def main(args):
    """
    Parse command-line arguments and start Luna accordingly.

    :param list[str] args: The list of command-line arguments.
    :return: The exit status code (0 for success, 1 for error).
    :rtype: int
    """

    if len(args) > 4:
        print("Error: Too many arguments, use -h for more information")
        return 1

    debug = False
    file = None
    mode = "Vocal"
    widget_mode = False

    for arg in args[1:]:
        if arg == "-h":
            display_help()
            return 0
        elif arg == "-d":
            debug = True
        elif arg == "-i":
            mode = "Input"
        elif arg == "-w":
            widget_mode = True
        elif arg.startswith("-"):
            print(f"Error: Unknown option '{arg}', use -h for more information")
            return 1
        else:
            if file is not None:
                print("Error: Too many arguments, use -h for more information")
                return 1
            file = arg

    if widget_mode:
        run_widget_mode(debug=debug)
    elif file:
        run_file_mode(file, debug=debug)
    else:
        run_mode(mode=mode, debug=debug)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
