import random
from mimesis import Person, Code

from ..common import Database, postgres_upsert
from .model import Employee, employee_bonus_view


def generate_initial_date(obs=50):
    data = []
    for i in range(1, obs):
        first_name = Person().name()
        last_name = Person().last_name()
        item = {
            'id': i,
            'first_name': first_name,
            'last_name': last_name,
            'company_id': Code().pin(mask='##-####-######'),
            'title': Person().occupation(),
            'email': f"{first_name}.{last_name}@company.com",
            'salary': random.randint(55000, 160000),
            'performance_score': random.normalvariate(2.5, 1),
        }
        data.append(item)
    return data


if __name__ == "__main__":
    db = Database(echo=True)
    if db.table_exists(Employee):
        db.drop_table(Employee)
    db.create_table(Employee)
    postgres_upsert(db.session, Employee, generate_initial_date())
    db.engine.execute(employee_bonus_view)
