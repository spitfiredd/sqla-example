from sqlalchemy import Column, Integer, Text, Index, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.sql import func
from sqlalchemy import DDL, event




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


def build_tsvector_trigger():
    # use postgres built in trigger tsvector_update_trigger
    # https://www.postgresql.org/docs/10/functions-textsearch.html
    trig_searchable_tsvector_stmt = """
    CREATE TRIGGER trig_searchable_tsvector BEFORE INSERT OR UPDATE
    ON company
    FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(
        searchable,'pg_catalog.english', 'name', 'about'
    )
    """
    trig_searchable_tsvector = DDL(trig_searchable_tsvector_stmt)

    event.listen(
        Company.__table__,
        'after_create',
        trig_searchable_tsvector.execute_if(dialect='postgresql')
    )
