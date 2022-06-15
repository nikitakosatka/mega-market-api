from fastapi import FastAPI, Request, APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from megamarket.schemas import Error
from megamarket.utils import InvalidRequestException, NotFoundException


def create_middleware(app: FastAPI):
    @app.exception_handler(InvalidRequestException)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(Error(code=400, message=str(exc)).dict(),
                            status_code=400)

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request, exc):
        return JSONResponse(Error(code=404, message=str(exc)).dict(),
                            status_code=404)
