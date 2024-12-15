from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app import file_processing_router
from app.core.exceptions import register_exception_handler

app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url="/docs",
    redoc_url=None,
    root_path='/api'
)
register_exception_handler(app)

app.include_router(file_processing_router, prefix="/files", tags=["Files"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
