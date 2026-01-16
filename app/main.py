from fastapi import Body, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from app.api.routes import users, auth, test
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler, validation_exception_handler, generic_exception_handler

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(test.router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)





