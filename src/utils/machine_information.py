import os
import platform
import re

def generate_acronym(exec):
    """
    Generate an acronym from a given executable name.

    :param str exec: The name of the executable.
    :return: The acronym generated from the input name.
    :rtype: str
    """
    words = re.split(r'[\s_]+', exec)
    return ''.join(word[0] for word in words if word).upper()

def normalizer_exec(exec):
    """
    Normalize an executable name by formatting and cleaning it.

    :param str exec: The name of the executable.
    :return: The normalized executable name.
    :rtype: str
    """
    exec = (exec.replace('\xa0', ' ')).split('.')[0]
    exec = re.sub(r'(?<!^)([A-Z])', r' \1', exec)
    exec = ' '.join(exec.lower().strip().split())
    exec = re.sub(r"\s+'", "'", exec)
    exec = re.sub(r"'\s+", "'", exec)
    return exec

def get_desktop_path():
    """
    Get the path to the user's desktop directory.

    :return: The path to the desktop.
    :rtype: str
    """
    if platform.system() == "Windows":
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def list_exec_desktop(desktop):
    """
    List executable files found on the user's desktop.

    :param str desktop: The path to the desktop directory.
    :return: A list of executable files or an error message if no executables are found.
    :rtype: list[str]
    """
    execs = []

    if not os.path.exists(desktop):
        return ["Erreur : Impossible d'accéder au Bureau"]
    
    for exec in os.listdir(desktop):
        file_path = os.path.join(desktop, exec)
        if platform.system() == "Windows" and (exec.endswith('.exe') or exec.endswith('.lnk') or exec.endswith('.url')):
            execs.append(exec)
        elif platform.system() != "Windows" and (os.access(file_path, os.X_OK) and os.path.isfile(file_path)) or exec.endswith('.desktop'):
            execs.append(exec)
    if not execs:
        return ["Erreur : Aucun exécutable trouvé sur le Bureau"]
    return execs