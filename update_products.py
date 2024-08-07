import os
import requests
import base64
import xml.etree.ElementTree as ET
import re

# Настройки для API
url = "http://ka2.sibzapaska.ru/API/hs/v1/product"
username = "API_client"
password = "rWp7mFWXRKOq"

# Создание заголовка для Basic Auth
auth = base64.b64encode(f"{username}:{password}".encode()).decode()

# Выполнение запроса к API
response = requests.get(url, headers={"Authorization": f"Basic {auth}"})
response.raise_for_status()  # Проверка на наличие ошибок

# Обработка ответа в формате JSON
data = response.json()

# Создание корневого элемента XML
root = ET.Element("Products")

# Преобразование каждого товара в XML элемент
for item in data:
    product = ET.SubElement(root, "Product")
    for key, value in item.items():
        if key != "Оптовая_Цена":  # Исключаем поле "Оптовая_Цена"
            element = ET.SubElement(product, key)
            element.text = str(value)

    # Определение тега для товара
    nomenclature = item.get("Номенклатура", "")
    if re.match(r'^(1[2-9]|2[0-4])\s', nomenclature):
        product.tag = "disk"
    else:
        product.tag = "tyres"

# Создание дерева XML и запись в файл
tree = ET.ElementTree(root)
with open("products.xml", "wb") as file:
    tree.write(file, encoding="utf-8", xml_declaration=True)

print("XML файл успешно создан.")
