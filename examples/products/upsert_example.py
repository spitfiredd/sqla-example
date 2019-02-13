import random
from mimesis import Business, Food

from .products import Product
from ..common import Database, postgres_upsert


def generate_initial_date(obs=50):
    data = []
    for i in range(1, obs):
        in_stock = random.choice([True, False])
        item = {
            'id': i,
            'name': random.choice([Food().fruit(), Food().vegetable()]),
            'in_stock': in_stock,
            'quantity': random.randint(1, 20) if in_stock else 0,
            'price': round(random.uniform(0.89, 3.99), 2)
        }
        data.append(item)
    return data


if __name__ == "__main__":
    db = Database(echo=True)
    if db.table_exists(Product):
        db.drop_table(Product)
    db.create_table(Product)
    postgres_upsert(db.session, Product, generate_initial_date())
