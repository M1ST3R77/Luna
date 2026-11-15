from datetime import datetime
from utils.get_timezone_from_str import get_timezone, jours_semaine, mois_annee

def get_date(launch, sentence):
    """
    Retrieves and announces the current date based on the detected timezone.

    This function extracts the timezone from the given sentence, obtains the 
    current date, and formats it into a spoken response. The date is 
    then read aloud using the audio system of the `Launch` instance.

    :param Launch launch: The main application instance.
    :param str sentence: The input sentence from which the timezone is determined.
    """
    timezone = get_timezone(sentence)
    date = datetime.now(timezone)
    jours = jours_semaine[date.weekday()]
    mois = mois_annee[date.month - 1]

    launch.audio.speak(f"le {jours} {date.day} {mois} {date.year}") 