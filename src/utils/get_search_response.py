from bs4 import BeautifulSoup
from groq import Groq
import requests
import re

def get_response(url, key):
    """
    Fetches and summarizes content from a given URL using Groq API.

    :param str url: The website URL to fetch.
    :param str key: API key for Groq.
    :return: Summary of the page content or an error message.
    :rtype: str
    """
    response = requests.get(url)
    if response.status_code != 200:
        return f"Une erreur est survenu lors de votre requête, accès impossible au site"
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find("script", language="JavaScript")
    if script:
        match = re.search(r'location\.replace\("(.*?)"\)', script.string)
        if match:
            url = match.group(1)
            response = requests.get(url)
            if response.status_code != 200:
                return f"Une erreur est survenu lors de votre requête, accès impossible au contenu du site"

    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(p.get_text() for p in soup.find_all("p"))[:2000]
    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Tu es maintenant un expert pour donner des résumés courts et concis, en évitant de mettre des * pour la présentation",},
            {"role": "user", "content": text,}

        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def search_web(research):
    """
    Searches DuckDuckGo and returns the first few results.

    :param str query: The search query.
    :return: A list of search results or an error message.
    :rtype: list | str
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": research}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Une erreur est survenu lors de votre requête, aucune recherche n'a pu aboutir"
    soup = BeautifulSoup(response.text, 'html.parser')
    res = []
    for result in soup.find_all("a", class_="result__a"):
        title = result.get_text()
        link = result['href']
        res.append({"title": title, "link": link})
    if res:
        return res
    else:
        return f"Une erreur est survenu lors de votre requête, aucun résultat n'a été trouvé"