from sqlalchemy import Column, String
from db.connector import Base

class Listing(Base):
    __tablename__ = "listing"

    id = Column(String, primary_key=True, index=True)
    vehicle_id = Column(String, nullable=False)
    url = Column(String, nullable=False)
    price = Column(String, nullable=False)
    kms = Column(String, nullable=False)