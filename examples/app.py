from .products import Product
from .common import session_factory


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


def populate_database():
    session = session_factory()
    for item in products:
        prod = Product(
            name=item['name'],
            in_stock=item['in_stock'],
            quantity=item['quantity'],
            price=item['price']
        )
        session.add(prod)
    session.commit()


def get_products():
    session = session_factory()
    return session.query(Product).all()


if __name__ == "__main__":
    prods = get_products()
    if len(prods) == 0:
        populate_database()
    prods = get_products()

    for p in prods:
        print(f'{p.name} is in stock {p.in_stock}')
        print(f'{p.name} costs {p.price}')
        print(f'{p.name} has {p.price} in stock')
