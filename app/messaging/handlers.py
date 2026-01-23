import logging
from app.database import SessionLocal
from app.models.motorcycle_notification import MotorcycleNotification

logger = logging.getLogger("motorcycle_notifications")

def handle_motorcycle_created(event: dict) -> None:
    year = int(event.get("year", 0))
    
    if year == 2024:
        notify_motorcycle_2024(event)

def notify_motorcycle_2024(event: dict) -> None:
    logger.info(
        "Motorcycle 2024 detected | id = %s model = %s",
        event["motorcycle_id"],
        event["model"]
    )

    db = SessionLocal()

    try: 
        notification = MotorcycleNotification(
            motorcycle_id = event["motorcycle_id"],
            model = event["model"],
            year = event["year"],
            vin = event["vin"]
        )
        db.add(notification)
        db.commit()

    finally:
        db.close()