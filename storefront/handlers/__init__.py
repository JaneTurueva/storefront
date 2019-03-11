from .companies import CompanyView, CompaniesView
from .employees import (
    EmployeeView, EmployeesView, EmployeeProductsView,
    EmployeeProductDeleteView
)
from .products import ProductView, ProductsView


HANDLERS = (
    CompanyView, CompaniesView,
    EmployeeView, EmployeesView, EmployeeProductsView,
    EmployeeProductDeleteView,
    ProductView, ProductsView
)
