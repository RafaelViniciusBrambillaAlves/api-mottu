from sqlalchemy import Column, Integer, Numeric
from app.database import Base

class RentalPlan(Base):
    __tablename__ = "rental_plans"

    id = Column(Integer, primary_key = True, index = True)

    days = Column(Integer, nullable = False, unique = True)
    price_per_day = Column(Numeric(10, 2), nullable = False)



