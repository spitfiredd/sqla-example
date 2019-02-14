from sqlalchemy import Column, Text, Numeric, Integer
from sqlalchemy.sql import select

from ..common import Base, Database
from ..surrogate import SurrogatePK

from .views import create_view


class Employee(Base, SurrogatePK):
    __tablename__ = 'employees'

    first_name = Column(Text)
    last_name = Column(Text)
    company_id = Column(Text)
    title = Column(Text)
    email = Column(Text)
    salary = Column(Numeric(8, 2))
    performance_score = Column(Numeric(4, 2))


class EmployeeBonusView(Base):
    bonus_view = create_view(
        'employee_bonus_view',
        Database().metadata,
        select(
            [
                Employee.id,
                (Employee.salary * 0.15).label('bonus_opportunity'),
                (Employee.salary * 0.15 * Employee.performance_score).label('bonus')
            ]
        )
    )
    __table__ = bonus_view

# Finishe tomorrow
# class EmployeeBonusView(Base):
#     __table__ = create_materialized_view(
#         'mv_employee_bonus',
#         #TODO: enter a query here.
#     )
