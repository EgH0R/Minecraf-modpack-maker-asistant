import openai
import os
import requests
from bs4 import BeautifulSoup

# Загрузка ключа из переменной окружения (или файл .env, если используется)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Функция для общения с GPT
def chat_with_gpt(user_input):
    completion = openai.Completion.create(
        model="gpt-3.5-turbo",  # Выбираем модель GPT-3
        prompt=user_input,
        max_tokens=150
    )
    return completion.choices[0].text.strip()

# Функция для поиска модов на проверенных сайтах
def search_mods(query):
    # Переводим запрос в теги для поиска
    user_input = f"Ищи моды для Minecraft по запросу: {query}"

    # Отправляем запрос в ChatGPT для получения тегов
    tags = chat_with_gpt(user_input)

    # Здесь можно сделать запросы к сайтам Modrinth и CurseForge, используя найденные теги
    mods = []

    # Примерный запрос на сайт Modrinth
    url = f"https://api.modrinth.com/v2/search?query={tags}&facets={{}}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for mod in data.get("hits", []):
            mods.append({
                "name": mod["title"],
                "url": mod["url"]
            })

    # Примерный запрос на сайт CurseForge
    url = f"https://api.curseforge.com/v1/mods/search?search={tags}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for mod in data.get("data", []):
            mods.append({
                "name": mod["name"],
                "url": mod["downloadUrl"]
            })

    # Возвращаем список найденных модов
    return mods

# Функция для вывода найденных модов
def display_mods(mods):
    if mods:
        print("Найдено модов:", len(mods))
        for mod in mods:
            print(f"{mod['name']}: {mod['url']}")
    else:
        print("Моды не найдены!")

def main():
    # Запрашиваем описание мода
    user_input = input("Опиши мод, который ты хочешь найти: ")

    # Ищем моды по описанию
    mods = search_mods(user_input)

    # Выводим найденные моды
    display_mods(mods)

if __name__ == "__main__":
    main()
