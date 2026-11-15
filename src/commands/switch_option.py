def switch_option(launch, sentence):
    """
    Switches the application option based on the command.

    :param Launch launch: The main application instance.
    :param str sentence: The command indicating the desired option.
    """
    if "normal" in sentence or "normale" in sentence:
        launch.switch_opt("Normal")
    elif "debug" in sentence:
        launch.switch_opt("Debug")
    else:
        launch.switch_opt(None)
    launch.audio.speak(f"L'option a été modifié pour : '{launch.option}'")