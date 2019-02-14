from sqlalchemy import Column, Text, Numeric
from sqlalchemy.sql import select

from ..common import Base
from ..surrogate import SurrogatePK

from .views import CreateView


class Employee(Base, SurrogatePK):
    __tablename__ = 'employees'

    first_name = Column(Text)
    last_name = Column(Text)
    company_id = Column(Text)
    title = Column(Text)
    email = Column(Text)
    salary = Column(Numeric(8, 2))
    performance_score = Column(Numeric(4, 2))


employee_bonus_view = CreateView(
    'employee_bonus_view',
    select(
        [
            Employee.id,
            (Employee.salary * 0.15).label('bonus_opportunity'),
            (Employee.salary * 0.15 * Employee.performance_score).label('bonus')
        ]
    )
)
