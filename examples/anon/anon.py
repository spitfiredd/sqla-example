from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..common import Base
from ..surrogate import SurrogatePK


class Anon(SurrogatePK, Base):
    __tablename__ = 'anon'

    # id = Column(Integer, primary_key=True)
    name = Column(String)
    ssn = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    reference = relationship('User', back_populates='other')
