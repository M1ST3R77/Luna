from datetime import datetime
from utils.get_timezone_from_str import get_timezone

def get_hours(launch, sentence):
    """
    Retrieves and announces the current time based on the detected timezone.

    This function extracts the timezone from the given sentence, gets the 
    current time, and formats it into a spoken response. The time is then 
    read aloud using the audio system of the `Launch` instance.

    :param Launch launch: The main application instance.
    :param str sentence: The input sentence from which the timezone is determined.
    """
    timezone = get_timezone(sentence)
    date = datetime.now(timezone)
    hour = date.hour
    minute = date.minute

    launch.audio.speak(f"{hour} heures {minute:02d}")