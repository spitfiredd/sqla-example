import os

from sqlalchemy import create_engine, inspect, UniqueConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

'''
Visit https://www.elephantsql.com/ if you need an quick and simple Postgres
instance. Same guys who brought you CloudAMPQ, I choose them because I liked
how they named their instances.
'''
DATABASE_URL = os.getenv('ELEPHANT_DATABASE_URI', default='sqlite:///sample.db')

engine = create_engine(DATABASE_URL, echo=True)

_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


class Database:
    """ Wrapper class for working with sqlalchemy sessions.

    Args:
        echo (bool): Turns on sqlalchemy echo options, useful for debugging
        queries.

    Attributes:
        url (str): Database url string, should be stored in env variable,
        defaults to `'sqlite:///sample.db'`
        echo (bool): Turns on sqlalchemy echo options, useful for debugging
        queries.

    """
    url = os.getenv('ELEPHANT_DATABASE_URI', default=None)

    def __init__(self, echo=False):
        if not self.url:
            raise ValueError("ELEPHANT_DATABASE_URI not set, use postgres URL.")
        self.echo = echo

    @property
    def engine(self):
        return create_engine(self.url, echo=self.echo)

    @property
    def session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def drop_table(self, model):
        """Drop table

        Args:
            model (`sqlalchemy.ext.declarative.api.DeclarativeMeta`):
            Sqlalchemy orm model.
        """
        model.__table__.drop(self.engine)

    def create_table(self, model):
        """Create table

        Args:
            model (`sqlalchemy.ext.declarative.api.DeclarativeMeta`):
            Sqlalchemy orm model.
        """
        model.__table__.create(self.engine)

    def table_exists(self, model):
        """
        Check if a table exists.

        Args:
            model (`sqlalchemy.ext.declarative.api.DeclarativeMeta`):
            Sqlalchemy orm model.

        Returns:
            bool: true if the table exists, other false.
        """
        table = model.__tablename__
        exists = self.engine.dialect.has_table(self.engine, table)
        return exists


def drop_table(model, engine=engine):
    model.__table__.drop(engine)


def create_table(model, engine=engine):
    model.__table__.create(engine)


def session_factory(create=True):
    if create:
        Base.metadata.create_all(engine)
    return _SessionFactory()


def postgres_upsert(session, model, rows):
    '''Postgres upsert (wont work on other databases)

    Args:
        session (sqlalchemy session): Sqlachemy Session
        model (sqlachemy.orm Model): Orm Model for the table you want to upsert
        records.
        rows (list): list of dict for rows to upsert, must include primary key.

    Raises:
        ValueError: update_dict is empty

    Returns:
        None: No return value, execute upsert and ends.
    '''

    table = model.__table__
    stmt = postgresql.insert(table)
    primary_keys = [key.name for key in inspect(table).primary_key]
    # update_dict = {c.name: c for c in table.columns if not c.primary_key}
    update_dict = {c.name: c for c in stmt.excluded if not c.primary_key}

    if not update_dict:
        raise ValueError("insert_or_update resulted in an empty update_dict")

    stmt = stmt.on_conflict_do_update(
        index_elements=primary_keys,
        set_=update_dict
    )

    seen = set()
    foreign_keys = {col.name: list(col.foreign_keys)[0].column for col in table.columns if col.foreign_keys}
    unique_constraints = [c for c in table.constraints if isinstance(c, UniqueConstraint)]

    def handle_foreignkeys_constraints(row):
        for c_name, c_value in foreign_keys.items():
            foreign_obj = row.pop(c_value.table.name, None)
            row[c_name] = getattr(foreign_obj, c_value.name) if foreign_obj else None

        for const in unique_constraints:
            unique = tuple([const, ] + [row[col.name] for col in const.columns])
            if unique in seen:
                return None
            seen.add(unique)

        return row

    rows = list(filter(None, (handle_foreignkeys_constraints(row) for row in rows)))
    session.execute(stmt, rows)
    session.commit()
