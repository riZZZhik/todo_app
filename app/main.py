"""FastAPI ToDo web application."""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from .api.errors import http422_error_handler, http_error_handler
from .api.routes.api import router as api_router


def get_application() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI()

    app.include_router(api_router)

    app.add_exception_handler(HTTPException, http_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(
        RequestValidationError, http422_error_handler  # type: ignore[arg-type]
    )

    return app


app = get_application()
