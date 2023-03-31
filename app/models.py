from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from datetime import datetime


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    operating_hours = Column(String)


class OperatingTime(Base):
    __tablename__ = "operating_time"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    start_min = Column(Integer)
    end_min = Column(Integer)

