from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import Base


class Province(Base):
    __tablename__ = 'provinces'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cities = relationship("City", back_populates="province")


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    province_id = Column(Integer, ForeignKey('provinces.id'))
    province = relationship("Province", back_populates="cities")
    # ⛔ Hapus baris ini:
    # properties = relationship("Property", back_populates="location")


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    location = Column(String(100))        # ✅ lokasi dari RajaOngkir
    province = Column(String(100))        # ✅ provinsi dari RajaOngkir
    price = Column(Float, nullable=False)
    building_size = Column(Integer)
    num_rooms = Column(Integer)
    type = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    fitur = Column(String(255))
    gambar = Column(String(255))
