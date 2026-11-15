from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
import ssl
import certifi

def get_city_from_str(text):
    """
    Extracts a city name from a given text using geolocation.

    :param str text: The input text containing a potential city name.
    :return: The detected city name or an error message.
    :rtype: str
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geolocator = Nominatim(user_agent="city_extractor", timeout=10, ssl_context=ssl_context)

    words = text.split()
    for w in words:
        try:
            loc = geolocator.geocode(w, exactly_one=True, language="fr")
            if loc:
                if loc.raw.get("name").lower() == w.lower() and (loc.raw.get("addresstype") == "city" or loc.raw.get("addresstype") == "suburb"):
                    return loc.raw.get("name")
        except GeopyError:
            continue
    return f"Une erreur est survenu durant la recherche de votre ville"