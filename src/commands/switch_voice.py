def switch_voice(launch, sentence):
    """
    Changes the voice setting based on the command.

    :param Launch launch: The main application instance.
    :param str sentence: The command indicating the desired voice.
    """
    res = None
    if "homme" in sentence or "d'homme" in sentence:
        res = launch.audio.change_voice("male")
    elif "femme" in sentence:
        res = launch.audio.change_voice("female")
    else:
        res = launch.audio.change_voice()
    voice = "de femme" if launch.audio.voice == "female" else "d'homme"
    if res:
        launch.audio.speak(f"La voix a été modifié pour une voix {voice}")
    else:
        launch.audio.speak(f"L'audio n'a pas été activé")