from babel import Locale
import pytz
import pycountry

jours_semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
mois_annee = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

def get_country_french(country):
    """
    Get the French name and country code for a given country.

    :param str country: The name of the country in English.
    :return: A tuple containing the French name of the country and its ISO 3166-1 alpha-2 code.
    :rtype: tuple[str, str | None]
    """
    try:
        c_obj = pycountry.countries.lookup(country)
        c_code = c_obj.alpha_2
    except LookupError:
        return country, None

    locale = Locale.parse('fr')
    country_name = locale.territories.get(c_code)
    return country_name, c_code

def get_country(text):
    """
    Extract the country code from a given text.

    :param str text: The input text containing a country name.
    :return: The ISO 3166-1 alpha-2 country code. Defaults to 'FR' if no match is found.
    :rtype: str
    """
    for country in pycountry.countries:
        country_name, country_code = get_country_french(country.name.lower())
        if country_name.lower() in text.lower():
            return country_code
    return "FR"

def get_timezone(sentence):
    """
    Determine the timezone based on the country mentioned in a sentence.

    :param str sentence: The input text containing a country name.
    :return: A timezone object corresponding to the detected country.
    :rtype: datetime.tzinfo
    """
    country_code = get_country(sentence)
    if country_code == "FR":
        timezone = pytz.timezone("Europe/Paris")
    else:
        timezone = pytz.timezone(pytz.country_timezones.get(country_code, ["Europe/Paris"])[0])
    return timezone