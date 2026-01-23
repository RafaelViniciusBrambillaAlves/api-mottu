from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime, timezone

class MotorcycleNotification(Base):
    __tablename__ = "motorcycle_notifications"

    id = Column(Integer, primary_key = True, index = True)
    motorcycle_id = Column(Integer, nullable = False)
    model = Column(String, nullable = False)
    year = Column(Integer, nullable = False)
    vin = Column(String, unique = True, index = True, nullable = False)
    received_at = Column(DateTime(timezone = True), default = datetime.now(timezone.utc))