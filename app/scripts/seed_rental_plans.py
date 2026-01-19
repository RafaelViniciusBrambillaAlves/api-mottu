from app.database import SessionLocal
from app.models.rental_plan import RentalPlan

PLANS = [
    {"days": 7, "price_per_day": 30.00},
    {"days": 15, "price_per_day": 28.00},   
    {"days": 30, "price_per_day": 22.00},
    {"days": 45, "price_per_day": 20.00},
    {"days": 50, "price_per_day": 18.00},
]

def seed():
    db = SessionLocal()

    for plan in PLANS:
        exits = db.query(RentalPlan).filter_by(days = plan["days"]).first()

        if not exits:
            db.add(RentalPlan(**plan))
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
