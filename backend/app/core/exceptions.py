import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core import logging_config  # noqa: F401

logger = logging.getLogger(__name__)


class ExceptionHandler:
    """
    Класс с методами для обработки возникающих исключений
    Возникшие исключения выводятся в консоль
    """

    @staticmethod
    async def log_exception(status_code, request, error):
        try:
            request_data = await request.json()
        except Exception:
            request_data = "No JSON data"
        logger.exception({
            "status_code": status_code,
            "request.url.path": request.url.path,
            "error": error,
            "request_data": request_data,
        })

    @staticmethod
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """Метод для обработки исключений, связанных с валидацией данных"""
        await ExceptionHandler.log_exception(422, request, exc.errors())
        error_info = exc.errors()[0]
        return JSONResponse(
            status_code=422,
            content={"detail": f"{error_info.get("loc", [])[-1]} - {error_info.get("msg", "error")}"},
        )

    @staticmethod
    async def handle_general_exception(request: Request, exc: Exception):
        """Обработчик любых других возникающих исключений"""
        await ExceptionHandler.log_exception(500, request, exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Внутренняя ошибка сервера"},
        )


def register_exception_handler(app: FastAPI):
    """Функция для установки правил при возникновении исключений"""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return await ExceptionHandler.handle_validation_error(request, exc)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return await ExceptionHandler.handle_general_exception(request, exc)
