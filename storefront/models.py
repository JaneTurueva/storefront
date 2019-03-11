from sqlalchemy import (
    MetaData, DateTime, Column, text, Integer, String,
    ForeignKey,
    DECIMAL)
from sqlalchemy.ext.declarative import as_declarative, declared_attr


def get_column_names(constraint, table) -> str:
    return '_'.join([
        column.name for column in constraint.columns.values()
    ])


convention = {
    'all_column_names': get_column_names,
    'ix': 'ix__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


@as_declarative(metadata=metadata)
class Base:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True),
                      server_default=text('clock_timestamp()'),
                      nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True),
                      server_default=text('clock_timestamp()'),
                      onupdate=text('clock_timestamp()'),
                      nullable=False)


class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.company_id'),
                        nullable=False)


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(precision=5, scale=2), nullable=False)


class EmployeeProductRelation(Base):
    __tablename__ = 'employee_product_relations'
    employee_id = Column(Integer, ForeignKey('employees.employee_id'),
                         primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'),
                        primary_key=True)
    created_at = None
    updated_at = None
