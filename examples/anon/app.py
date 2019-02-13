import random
from mimesis import Person
from mimesis.enums import Gender
from mimesis.builtins import USASpecProvider

from .anon import Anon
from .users import User

from ..common import Database


def populate_database(session):
    genders = [Gender.FEMALE, Gender.MALE]
    for _ in range(5):
        gender = random.choice(genders)
        user = User(
            name=Person('en').full_name(gender=gender),
            ssn=USASpecProvider().ssn()
        )
        anon = Anon(
            name=Person('en').full_name(gender=gender),
            ssn=USASpecProvider().ssn(),
            reference=user
        )

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
