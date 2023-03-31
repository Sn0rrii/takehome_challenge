from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app import models


def get_restaurants(db: Session, dt: datetime) -> List[models.Restaurant]:
    minute_of_week = dt.weekday() * 1440 + dt.hour * 60 + dt.minute

    return db.query(models.Restaurant).join(models.OperatingTime).filter(
        models.OperatingTime.start_min <= minute_of_week,
        models.OperatingTime.end_min > minute_of_week
    ).order_by(models.Restaurant.name).all()


def create_restaurant(db: Session, name: str, operating_hours: str) -> models.Restaurant:
    db_restaurant = models.Restaurant(name=name, operating_hours=operating_hours)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def create_operating_time_ranges(db: Session, ots: [models.OperatingTime]):
    for ot in ots:
        db.add(ot)
    db.commit()
