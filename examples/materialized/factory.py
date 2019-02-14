from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
from sqlalchemy import MetaData, Table, event, Column, DDL

class CreateMaterializedView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


@compiler.compiles(CreateMaterializedView)
def compile(element, compiler, **kwargs):
    return 'CREATE MATERIALIZED VIEW {} AS {}'.format(
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True)
    )


def create_materialized_view(name, selectable, metadata=MetaData()):
    t = Table(name, metadata)
    for c in selectable.c:
        t.append_column(Column(c.name, c.type, primary_key=c.primary_key))

    event.listen(
        metadata,
        'after_create',
        CreateMaterializedView(name, selectable)
    )

    event.listen(
        metadata,
        'before_drop',
        DDL('DROP MATERIALIZED VEIW IF EXISTS '.format(name))
    )
    return t
