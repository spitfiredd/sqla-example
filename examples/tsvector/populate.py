from faker import Faker

from .model import Company
from ..common import session_factory


fake = Faker()


def populate_database():
    session = session_factory()
    for _ in range(10):
        company = Company(
            name=fake.company(),
            address=fake.address(),
            city=fake.city(),
            state=fake.state(),
            about=fake.bs()
        )
        session.add(company)
    session.commit()


if __name__ == "__main__":
    populate_database()
