from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from .api.errors import http422_error_handler, http_error_handler
from .api.routes.api import router as api_router
from .database import TasksDatabase


def get_application() -> FastAPI:
    app = FastAPI()

    app.include_router(api_router)

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

    return app


app = get_application()
