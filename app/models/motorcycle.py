from sqlalchemy import Column, Integer, String
from app.database import Base

class Motorcycle(Base):
    __tablename__ = "motorcycles"

    id = Column(Integer, primary_key = True, index = True)
    model = Column(String, nullable = False)
    year = Column(Integer, nullable = False)
    vin = Column(String, unique = True, index = True, nullable = False)