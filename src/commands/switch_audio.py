def switch_audio(launch, sentence):
    """
    Enables or disables audio based on the command.

    :param Launch launch: The main application instance.
    :param str sentence: The command indicating whether to enable or disable audio.
    """
    if "désactive" in sentence:
        launch.audio.switch_audio(False)
    elif "active" in sentence:
        launch.audio.switch_audio(True)
    audio = "Activé" if launch.audio.audio == True else "Désactivé"
    launch.audio.speak(f"L'audio est maintenant : '{audio}'")