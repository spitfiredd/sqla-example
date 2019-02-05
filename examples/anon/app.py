from faker import Faker

from .anon import Anon
from .users import User

from ..common import session_factory


def populate_database():
    session = session_factory()
    fake = Faker()
    for _ in range(5):
        user = User(name=fake.name(), ssn=fake.ssn())
        anon = Anon(name=fake.name(), ssn=fake.ssn(), reference=user)

        session.add(anon)
    session.commit()


if __name__ == "__main__":
    populate_database()
