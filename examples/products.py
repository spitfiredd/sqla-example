from sqlalchemy import Column, Integer, Boolean, Numeric, String

from .common import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    in_stock = Column(Boolean)
    quantity = Column(Integer)
    price = Column(Numeric)
