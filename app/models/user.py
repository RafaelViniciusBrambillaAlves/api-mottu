from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)  

    name = Column(String(50), nullable = False)
    email = Column(String(255), unique = True, index = True, nullable = False)
    password = Column(String, nullable = False)

    role = Column(String(20), nullable = False, default = "user")

    cnpj = Column(String(20), unique = True, index = True, nullable = True)
    birthday = Column(String, nullable = True)
    cnh_number = Column(String, unique = True, index = True, nullable = True)
    cnh_type = Column(String, nullable = True)

    created_at = Column(DateTime(timezone = True), default = datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone = True), default = datetime.now(timezone.utc), onupdate = datetime.now(timezone.utc))
