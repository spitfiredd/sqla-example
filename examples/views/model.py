from sqlalchemy import Column, Text, Numeric

from ..common import Base
from ..surrogate import SurrogatePK

from .materialized import create_materialized_view


class Employee(Base, SurrogatePK):
    __tablename__ = 'employees'

    first_name = Column(Text)
    last_name = Column(Text)
    company_id = Column(Text)
    title = Column(Text)
    email = Column(Text)
    salary = Column(Numeric(8, 2))
    performance_score = Column(Numeric(4, 2))

# Finishe tomorrow
# class EmployeeBonusView(Base):
#     __table__ = create_materialized_view(
#         'mv_employee_bonus',
#         #TODO: enter a query here.
#     )
