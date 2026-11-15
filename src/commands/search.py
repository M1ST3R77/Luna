from utils.get_search_response import search_web, get_response
from utils.get_key_from_file import get_key

def search(launch, _):
    """
    Performs a web search and retrieves a response based on the user's input.

    :param Launch launch: The main application instance.
    :param _: Unused parameter, kept for compatibility with function calls.
    """
    key = get_key("groq_key")

    if "Erreur" in key:
        launch.audio.speak(key)
        return

    while True:
        sentence = launch.input.input_sentence("search")
        if sentence != None:
            break
    
    res_search = search_web(sentence)
    if "erreur" in res_search:
        launch.audio.speak(res_search)
        return
    res = get_response("https:" + res_search[0]['link'], key)
    launch.audio.speak(res)
    if "erreur" in res:
        return
    print("https:" + res_search[0]['link'])
