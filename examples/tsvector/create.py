from sqlalchemy import DDL, event

from .model import Company
from ..common import create_table


if __name__ == "__main__":
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
    # you have to create table after you create the triggers, I would do
    # some additional research about around this fact.
    create_table(Company)
