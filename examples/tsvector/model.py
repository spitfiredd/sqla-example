from sqlalchemy import Column, Integer, Text, Index, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.sql import func



from ..common import Base
from ..surrogate import SurrogatePK


def to_tsvector_ix(*columns):
    '''Helper function to create TSVector on multiple columns.

    Returns:
        str: column names, e.g. 'city', 'state', 'about', ect...
    '''
    s = " || ' ' || ".join(columns)
    return func.to_tsvector('english', text(s))


class Company(SurrogatePK, Base):
    __tablename__ = 'company'

    name = Column(Text)
    address = Column(Text)
    city = Column(Text)
    state = Column(Text)
    about = Column(Text)
    searchable = Column(TSVECTOR)

    __table_args__ = (
        Index(
            'ix_tsvector_company',
            searchable,
            postgresql_using="gin"
        ),
    )
