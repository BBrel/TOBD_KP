import re
from xml.etree import ElementTree
from datetime import datetime


class XMLProcessor:
    """
    Класс для манипуляции с XML-файлами, который содержит методы
    для преобразования XML в JSON и обратно.
    """

    @classmethod
    def determine_type(cls, value: str) -> str:
        """
        Определяет тип данных на основе значения.
        """
        if value.isdigit():
            return "number"
        try:
            float(value.replace(",", "."))
            return "number"
        except ValueError:
            pass
        if re.match(r"\d{4}-\d{2}-\d{2}", value):
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return "date"
            except ValueError:
                pass
        return "text"

    @classmethod
    def parse_element(cls, element: ElementTree.Element) -> dict:
        """
        Метод для преобразования содержимого XML-файла в JSON формат
        с рекурсивной обработкой вложенных элементов.
        """
        # Базовая структура с тегом
        data = {"tag": element.tag, "attributes": {}, "children": []}

        # Обрабатываем атрибуты
        for key, value in element.attrib.items():
            data["attributes"][key] = {"value": value, "type": cls.determine_type(value)}

        # Добавляем текст, если он есть
        if element.text and element.text.strip():
            data["text"] = {"value": element.text.strip(), "type": cls.determine_type(element.text.strip())}

        # Обрабатываем детей рекурсивно
        for child in element:
            data["children"].append(cls.parse_element(child))

        return data

    @classmethod
    def build_element(cls, data: dict) -> ElementTree.Element:
        """
        Метод для построения XML-файла на основе JSON,
        рекурсивно обрабатывая вложенные элементы.
        """
        # Получаем имя тега
        tag_name = data.get("tag", "item")
        attributes = {k: v["value"] for k, v in data.get("attributes", {}).items()}

        # Создаем элемент
        element = ElementTree.Element(tag_name, attrib=attributes)

        # Добавляем текст, если он есть
        if "text" in data and data["text"]["value"]:
            element.text = data["text"]["value"]

        # Обрабатываем дочерние элементы рекурсивно
        for child in data.get("children", []):
            element.append(cls.build_element(child))

        return element
