from .model import Company, build_tsvector_trigger
from ..common import create_table


if __name__ == "__main__":

    build_tsvector_trigger()
    # you have to create table after you create the triggers, I would do
    # some additional research about around this fact.
    create_table(Company)
