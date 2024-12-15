from xml.etree import ElementTree


class XMLProcessor:
    """
    Класс для манипуляции с XML-файлами, который содержит методы
    для преобразования XML в JSON и обратно
    """

    @classmethod
    def parse_element(cls, element: ElementTree.Element) -> dict:
        """
        Метод для преобразования содержимого XML-файла в JSON формат
        с рекурсивной обработкой вложенных элементов исходного файла
        """
        data = {"tag": element.tag, **element.attrib}

        # Добавляем текст, если он есть
        if element.text and element.text.strip():
            data["text"] = element.text.strip()

        # Обрабатываем детей
        children = [cls.parse_element(child) for child in element]
        if children:
            data["children"] = children

        return data

    @classmethod
    def build_element(cls, data: dict) -> ElementTree.Element:
        """
        Метод для построения XML-файла на основе JSON,
        рекурсивно обрабатывая вложенные элементы
        """
        # Получаем имя тега
        tag_name = data.get("tag", "item")  # По умолчанию "item", если нет "tag"

        # Собираем атрибуты из всех ключей, кроме "children", "text" и "tag"
        attributes = {key: value for key, value in data.items() if key not in ("tag", "text", "children")}
        element = ElementTree.Element(tag_name, attrib=attributes)

        # Добавляем текст, если он есть
        text = data.get("text")
        if text:
            element.text = text

        # Обрабатываем дочерние элементы рекурсивно
        for child in data.get("children", []):
            element.append(cls.build_element(child))

        return element
