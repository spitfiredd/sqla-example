import os
import random

import pytest
import factory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from examples.common import Database
from examples.products.products import Product


DATABASE_URL = os.getenv('ELEPHANT_DATABASE_URI')

engine = create_engine(DATABASE_URL)
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    ProductFactory._meta.sqlalchemy_session = session # NB: This line added
    yield session
    session.close()
    transaction.rollback()


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: '%s' % n)
    name = factory.Faker('name')
    in_stock = random.choice([True, False])
    quantity = random.randint(0, 10)
    price = random.uniform(10., 30.)

    class Meta:
        model = Product


def delete_product_test(session, product_id):
    session.query(Product).filter(Product.id == product_id).delete()


def test_case(session):
    product = ProductFactory.create()
    assert session.query(Product).one()

    delete_product_test(session, product.id)

    result = session.query(Product).one_or_none()
    assert result is None
