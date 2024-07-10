import os
import requests
import base64
import xml.etree.ElementTree as ET

# Настройки для API
url = "http://ka2.sibzapaska.ru/API/hs/v1/product"
username = os.getenv("API_USERNAME", "API_client")
password = os.getenv("API_PASSWORD", "rWp7mFWXRKOq")

# Создание заголовка для Basic Auth
auth = base64.b64encode(f"{username}:{password}".encode()).decode()

try:
    print("Отправка запроса к API...")
    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(url, headers=headers)
    
    # Для отладки: выводим заголовки запроса и ответа
    print(f"Заголовки запроса: {response.request.headers}")
    print(f"Заголовки ответа: {response.headers}")
    
    response.raise_for_status()  # Проверка на наличие ошибок HTTP

    # Обработка ответа в формате JSON
    data = response.json()
    print(f"Получены данные: {data}")

    # Создание корневого элемента XML
    root = ET.Element("Products")

    # Преобразование каждого товара в XML элемент
    for item in data:
        product = ET.SubElement(root, "Product")
        for key, value in item.items():
            if key != "Оптовая_Цена":  # Исключаем поле "Оптовая_Цена"
                element = ET.SubElement(product, key)
                element.text = str(value)
    print("XML структура создана.")

    # Создание дерева XML и запись в файл
    tree = ET.ElementTree(root)
    with open("products.xml", "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)
    print("XML файл успешно создан.")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP ошибка: {http_err}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
    raise
