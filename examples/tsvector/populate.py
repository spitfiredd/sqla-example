from faker import Faker

from .model import Company, build_tsvector_trigger
from ..common import Database


fake = Faker()


def populate_database(session, nobs=10):
    for _ in range(nobs):
        company = Company(
            name=fake.company(),
            address=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            about=fake.bs()
        )
        session.add(company)
    session.commit()


if __name__ == "__main__":
    db = Database(echo=True)
    if db.table_exists(Company):
        db.drop_table(Company)
    build_tsvector_trigger()
    db.create_table(Company)
    populate_database(db.session)
