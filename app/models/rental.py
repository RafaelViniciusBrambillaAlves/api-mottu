from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from datetime import datetime, timezone

from app.database import Base

class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key = True, index = True) 

    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    motorcycle_id = Column(Integer, ForeignKey("motorcycles.id"), nullable = False)

    start_date = Column(Date, nullable = False)
    expected_end_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = True)

    status = Column(String(20), nullable = False, default = "active")

    created_at = Column(DateTime(timezone = True), default = datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone = True), default = datetime.now(timezone.utc), onupdate = datetime.now(timezone.utc))


