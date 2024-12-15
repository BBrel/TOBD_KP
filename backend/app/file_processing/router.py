from io import BytesIO
from xml.etree import ElementTree

from fastapi import UploadFile, APIRouter
from fastapi.responses import JSONResponse
from starlette import status
from starlette.responses import StreamingResponse

from .schemas import SaveRequest
from .xml_processor import XMLProcessor

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_xml(file: UploadFile):
    try:
        tree = ElementTree.parse(file.file)
        root = tree.getroot()

        # Парсим XML
        parsed_data = XMLProcessor.parse_element(root)
        return JSONResponse(
            status_code=200,
            content={"data": [parsed_data]}
        )

    except ElementTree.ParseError as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Ошибка чтения файла: {str(e)}"}
        )


@router.post("/save", status_code=status.HTTP_200_OK)
async def save_xml(request: SaveRequest):
    """
    Принимает JSON-данные и возвращает собранный XML-файл.
    """
    try:
        # Проверяем наличие данных
        if not request.data or len(request.data) == 0:
            raise ValueError("Нет данных для сохранения")

        # Используем первый элемент как корневой
        root_data = request.data[0]
        root = XMLProcessor.build_element(root_data)

        # Генерация XML-строки
        xml_data = ElementTree.tostring(root, encoding="utf-8", method="xml").decode("utf-8")

        # Возвращаем XML-файл пользователю
        return StreamingResponse(
            BytesIO(xml_data.encode("utf-8")),
            media_type="application/xml"
        )

    except (TypeError, ValueError, AttributeError) as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Ошибка при сборке XML: {str(e)}"}
        )
