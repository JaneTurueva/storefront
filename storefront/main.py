from functools import partial
from types import MappingProxyType
from typing import Mapping

import os
from aiohttp import web, PAYLOAD_REGISTRY
from asyncpgsa import PG
from storefront.handlers import CompaniesView, CompanyView, EmployeesView, \
    EmployeeView, ProductsView, ProductView
from storefront.payloads import JsonPayload


MODULE_PATH = os.path.abspath(os.path.dirname(__file__))


async def setup_db(db_url: str, app):
    pg = PG()
    await pg.init(db_url)
    app['postgres'] = pg


def create_app(db_url: str):
    app = web.Application()

    setup_db_with_url = partial(setup_db, db_url)
    app.on_startup.append(setup_db_with_url)

    app.router.add_route('*', '/companies', CompaniesView)
    app.router.add_route('*', '/companies/{id}', CompanyView)
    app.router.add_route('*', '/employees', EmployeesView)
    app.router.add_route('*', '/employees/{id}', EmployeeView)
    app.router.add_route('*', '/products', ProductsView)
    app.router.add_route('*', '/products/{id}', ProductView)
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return app


def main():
    app = create_app('postgresql://api:hackme@0.0.0.0:5432/storefront')
    web.run_app(app)