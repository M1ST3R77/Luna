def switch_mode(launch, sentence):
    """
    Switches the input mode based on the command.

    :param Launch launch: The main application instance.
    :param str sentence: The command indicating the desired mode.
    """
    if "vocal" in sentence or "vocale" in sentence:
        launch.input.mode = "Vocal"
    elif "input" in sentence:
        launch.input.mode = "Input"
    else:
        launch.switch_mode()
    launch.audio.speak(f"Le mode a été modifié pour : '{launch.input.mode}'")