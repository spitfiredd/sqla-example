from faker import Faker

from .anon import Anon
from .users import User

from ..common import Database


def populate_database(session):
    fake = Faker()
    for _ in range(5):
        user = User(name=fake.name(), ssn=fake.ssn())
        anon = Anon(name=fake.name(), ssn=fake.ssn(), reference=user)

        session.add(anon)
    session.commit()


if __name__ == "__main__":
    db = Database(echo=True)
    # drop tables if they both exists
    if db.table_exists(Anon) and db.table_exists(User):
        db.drop_table(User)
        db.drop_table(Anon)
    db.create_table(User)
    db.create_table(Anon)
    populate_database(db.session)
