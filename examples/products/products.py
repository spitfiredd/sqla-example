from sqlalchemy import Column, Integer, Boolean, Numeric, String

from ..common import Base
from ..surrogate import SurrogatePK


class Product(SurrogatePK, Base):
    __tablename__ = 'products'

    # id = Column(Integer, primary_key=True)
    name = Column(String(32))
    in_stock = Column(Boolean)
    quantity = Column(Integer)
    price = Column(Numeric(6, 2))

    def __repr__(self):
        return f'<Product(name={self.name}, id={self.id})>'
