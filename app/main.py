from fastapi import Body, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from app.api.routes import users, admin, auth, test, motorcycles, rentals
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler, validation_exception_handler, generic_exception_handler
from app.core.kafka import KafkaProducer

async def lifespan(app: FastAPI):
    await KafkaProducer.start()
    yield
    await KafkaProducer.stop()


app = FastAPI(
    title="Mottu API",
    version="1.0.0",
    description="API for motorcycle rentals",
    lifespan = lifespan
)

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)

app.include_router(motorcycles.router)
app.include_router(rentals.router)

# app.include_router(test.router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)






