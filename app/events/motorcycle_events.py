from datetime import datetime, timezone
from app.models.motorcycle import Motorcycle

def motorcycle_created_event(motorcycle: Motorcycle) -> dict:
    return {
        "event": "MOTORCYCLE_CREATED",
        "motorcycle_id": motorcycle.id,
        "model": motorcycle.model,
        "vin": motorcycle.vin,
        "year": motorcycle.year,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

