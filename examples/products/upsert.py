from .products import Product
from ..common import session_factory


products = [
    {
        'name': 'Scissors',
        'in_stock': True,
        'quantity': 10,
        'price': 3.99
    },
    {
        'name': 'Stapler',
        'in_stock': False,
        'quantity': 0,
        'price': 7.99
    }
]

if __name__ == '__main__':
    session = session_factory()
    print('Initial state:\n')
    print(session.query(Product).all())
