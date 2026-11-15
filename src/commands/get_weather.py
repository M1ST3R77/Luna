import requests
from utils.get_city_from_str import get_city_from_str
from utils.get_key_from_file import get_key

def get_coordinates_city(city, key, launch):
    """
    Retrieves the latitude and longitude of a given city using OpenWeatherMap's Geocoding API.

    :param str city: The name of the city to retrieve coordinates for.
    :param str key: The API key for OpenWeatherMap.
    :param Launch launch: The main application instance responsible for handling audio output.

    :return: A tuple (latitude, longitude) if successful, otherwise None.
    :rtype: tuple or None
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            launch.audio.speak("Une erreur est survenu lors de votre requête, aucune donnée n'a été trouvé pour cette ville")
            return None
    else:
        launch.audio.speak("Une erreur est survenu lors de votre requête, connection compromise avec l'API")
        return None

def get_weather(launch, sentence):
    """
    Retrieves and announces the current weather conditions for a detected city.

    This function extracts the city name from the input sentence, fetches its coordinates,
    and retrieves the weather data using OpenWeatherMap's API. The weather conditions 
    are then read aloud.

    :param Launch launch: The main application instance.
    :param str sentence: The input sentence from which the city name is extracted.
    """
    city = get_city_from_str(sentence)
    url = "https://api.openweathermap.org/data/2.5/weather"
    key = get_key("weather_key")

    if "Erreur" in key:
        launch.audio.speak(key)
        return

    if "erreur" in city:
        launch.audio.speak(city)
        return

    if launch.option == "Debug":
        print(f"[DEBUG] Here is the city detected : {city}")

    coor = get_coordinates_city(city, key, launch)
    if coor == None:
        return
    lat, lon = coor

    params = {
        "lat": lat,
        "lon": lon,
        "appid": key,
        "units": "metric",
        "lang": "fr"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        temp = round(float(data["main"]["temp"]))
        desc = data["weather"][0]["description"]
        launch.audio.speak(f"Pour {city}, if fait {temp}°C et voici le temps : {desc}")
    except:
        launch.audio.speak("Une erreur est survenu lors de votre requête, connection compromise avec l'API")