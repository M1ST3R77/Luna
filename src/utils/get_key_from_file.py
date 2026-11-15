import os

def get_key(file_name):
    """
    Retrieves an API key stored in a file.

    :param str file_name: Name of the file containing the API key.
    :return: The API key or an error message.
    :rtype: str
    """
    path = f'src/files/{file_name}'
    error = False

    if not os.path.exists(path):
        error = True
    else:
        with open(path, "r") as file:
            key = file.read().strip()
        
        if not key:
            error = True
    
    if error:
        return f"Erreur durant votre requête : Veuillez créer un fichier {file_name} dans le dossier files et y ajouter une clé d'API valide (OpenWeatherMap ou Groq par exemple)"
    else:
        return key