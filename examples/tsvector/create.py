from .model import Company, build_tsvector_trigger
from ..common import Database


if __name__ == "__main__":
    db = Database(echo=True)
    build_tsvector_trigger()
    # you have to create table after you create the triggers, I would do
    # some additional research about around this fact.
    db.create_table(Company)
