from sqlalchemy import Column, Integer, String, Float
from config import Base

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    location = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    building_size = Column(Integer)
    num_rooms = Column(Integer)
    type = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
