import requests

def search_mods(query):
    url = "https://api.curseforge.com/v1/mods/search"  # Пример API, если используешь CurseForge
    params = {"query": query}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем список модов
    else:
        return []  # Если не нашли модов
