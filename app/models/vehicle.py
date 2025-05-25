from sqlalchemy import Column, String, Integer
from db.connector import Base

class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    badge = Column(String, nullable=False)
    transmission_type = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    drive_type = Column(String, nullable=False)