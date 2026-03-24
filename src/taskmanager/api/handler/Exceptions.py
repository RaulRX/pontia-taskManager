from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.taskmanager.service.Service_exception import BadNoteException, DuplicationException, NotFoundException, NonWritableException, TextOverflowException


def _error_response(status_code: int, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": status_code, "detail": detail},
    )


def Exception_handler(app: FastAPI) -> None:

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return _error_response(status.HTTP_404_NOT_FOUND, str(exc))

    @app.exception_handler(BadNoteException)
    async def bad_note_handler(request: Request, exc: BadNoteException):
        return _error_response(status.HTTP_400_BAD_REQUEST, str(exc))

    @app.exception_handler(DuplicationException)
    async def duplication_handler(request: Request, exc: DuplicationException):
        return _error_response(status.HTTP_409_CONFLICT, str(exc))

    @app.exception_handler(TextOverflowException)
    async def text_overflow_handler(request: Request, exc: TextOverflowException):
        return _error_response(status.HTTP_400_BAD_REQUEST, str(exc))

    @app.exception_handler(NonWritableException)
    async def non_writable_handler(request: Request, exc: NonWritableException):
        return _error_response(status.HTTP_409_CONFLICT, str(exc))

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return _error_response(status.HTTP_400_BAD_REQUEST, str(exc))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        return _error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))