from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from ..common import Base
from ..surrogate import SurrogatePK


class User(SurrogatePK, Base):
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True)
    name = Column(String)
    ssn = Column(String)
    other = relationship('Anon', uselist=False, back_populates='reference')
