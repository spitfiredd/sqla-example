from .products import Product
from ..common import session_factory, postgres_upsert


products = [
    {
        'name': 'Scissors',
        'in_stock': True,
        'quantity': 20,
        'price': 3.99
    },
    {
        'name': 'Stapler',
        'in_stock': True,
        'quantity': 25,
        'price': 7.99
    }
]


def _upsert():
    session = session_factory()
    postgres_upsert(session, Product, ['in_stock', 'quantity', 'price'])


if __name__ == "__main__":
    # Install postgres first!
    _upsert()
