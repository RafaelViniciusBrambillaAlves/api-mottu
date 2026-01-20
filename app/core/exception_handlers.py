from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.schemas.error import ErrorResponse

def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code = exc.status_code,
        content = ErrorResponse(
            error = exc.error, 
            message = exc.message
        ).model_dump()
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code = 422,
        content = {
            "error": "VALIDATION_ERROR",
            "message": "Invalid data sent in the request",
        }
    )

def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code = 500, 
        content = {
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later"
        }
    )