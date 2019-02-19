from sqlalchemy.sql import text
from examples.views.views import CreateView, DropView


def test_create_view_query_strings():
    query = text("SELECT * FROM my_table")
    view = CreateView('my_view', query)
    view_string = str(view.compile())
    assert view_string == 'CREATE OR REPLACE VIEW my_view AS SELECT * FROM my_table'


def test_drop_view_cascade_query_strings():
    view = DropView('my_view')
    view_string = str(view.compile())
    assert view_string == 'DROP VIEW IF EXISTS my_view CASCADE'


def test_drop_view_no_cascade_query_string():
    view = DropView('my_view', cascade=False)
    view_string = str(view.compile())
    assert view_string == 'DROP VIEW IF EXISTS my_view'
