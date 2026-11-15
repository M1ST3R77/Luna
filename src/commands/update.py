def update(launch, _):
    """
    Triggers the update process.

    :param Launch launch: The main application instance.
    :param _: Unused parameter, kept for compatibility with function calls.
    """
    launch.update()
    launch.audio.speak("La mise à jour est terminé !")