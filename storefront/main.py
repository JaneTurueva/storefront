from types import MappingProxyType
from typing import Mapping

from aiohttp import web, PAYLOAD_REGISTRY
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp_swaggerify import swaggerify
from aiohttp_validate import validate
from asyncpg import UniqueViolationError
from asyncpgsa import PG
from storefront.handlers import CompaniesView, CompanyView, EmployeesView, \
    EmployeeView, ProductsView, ProductView
from storefront.payloads import JsonPayload
from storefront.models import Company, Employee


async def setup_db(app):
    pg = PG()
    await pg.init('postgresql://api:hackme@0.0.0.0:5432/storefront')
    app['postgres'] = pg


def main():
    app = web.Application()
    app.on_startup.append(setup_db)
    app.router.add_route('*', '/companies', CompaniesView)
    app.router.add_route('*', '/companies/{id}', CompanyView)
    app.router.add_route('*', '/employees', EmployeesView)
    app.router.add_route('*', '/employees/{id}', EmployeeView)
    app.router.add_route('*', '/products', ProductsView)
    app.router.add_route('*', '/products/{id}', ProductView)
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))

    web.run_app(app)