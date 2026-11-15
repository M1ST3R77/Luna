from utils.machine_information import get_desktop_path, list_exec_desktop, normalizer_exec, generate_acronym
import os
import platform
import subprocess
import re
import shutil

def find_exec(sentence, execs):
    """
    Finds the executable that best matches the given sentence.

    :param str sentence: The user input sentence.
    :param list execs: A list of executable names found on the desktop.

    :return: The name of the matched executable or None if no match is found.
    :rtype: str or None
    """
    exec_sentence = sentence.lower()
    execs_list = {}

    for exec in execs:
        exec_list = []
        normalized = normalizer_exec(exec).lower()
        exec_list.append(normalized)
        exec_list.append(generate_acronym(normalized).lower())

        for word in re.split(r'[\s_]+', normalized):
            exec_list.append(word)

        execs_list[exec] = exec_list

    for key, values in execs_list.items():
        if len(exec_sentence) > 1 and exec_sentence in values:
            return key

    return None

def launch_exec(launch, _):
    """
    Launches an application from the user's desktop based on voice input.

    :param Launch launch: The main application instance.
    :param _: Unused parameter, kept for compatibility with function calls.
    """
    desktop = get_desktop_path()
    execs = list_exec_desktop(desktop)

    if launch.option == "Debug":
        print(f"[DEBUG] desktop path = '{desktop}'")

    if "Erreur" in execs[0]:
        launch.audio.speak(execs[0])
        return

    if launch.option == "Debug":
        print(f"[DEBUG] executables list = {execs}")
    
    while True:
        sentence = launch.input.input_sentence("search")
        if sentence != None:
            break

    match_exec = find_exec(sentence, execs)
    if match_exec:
        exec = os.path.join(desktop, match_exec)
        if not os.path.exists(exec):
            launch.audio.speak("Une erreur est survenue, impossible d'accéder à l'application")
            return
        try:
            if platform.system() == "Windows":
                subprocess.Popen([exec], shell=True)
            else:
                if exec.endswith('.desktop'):
                    exec = os.path.realpath(exec)
                    gio_path = shutil.which("gio")
                    if not gio_path:
                        raise FileNotFoundError("Unable to find 'gio' on your system.")
                    else:
                        subprocess.Popen([gio_path, "launch", exec])
                else:
                    subprocess.Popen([exec], cwd=desktop)
            launch.audio.speak("L'application s'est lancée avec succès")
        except:
            launch.audio.speak("Une erreur est survenue durant le lancement de l'application")
    else:
        launch.audio.speak("Une erreur est survenue, l'application n'existe pas sur le Bureau")