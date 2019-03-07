from types import MappingProxyType
from typing import Mapping

from aiohttp import web, PAYLOAD_REGISTRY
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from asyncpg import UniqueViolationError
from asyncpgsa import PG
from storefront.payloads import JsonPayload
from storefront.models import Company


async def setup_db(app):
    pg = PG()
    await pg.init('postgresql://api:hackme@0.0.0.0:5432/storefront')
    app['postgres'] = pg


class BaseView(web.View):
    @property
    def postgres(self) -> PG:
        return self.request.app['postgres']


class CompaniesView(BaseView):
    TABLE = Company.__table__

    async def post(self):
        data = await self.request.json()
        query = self.TABLE.insert().values(name=data['name']).returning(
            self.TABLE
        )
        try:
            data = await self.postgres.fetchrow(query)
        except UniqueViolationError:
            raise HTTPConflict()

        return web.Response(body={'data':data})

    async def get(self):
        query = Company.__table__.select()
        data = await self.postgres.fetch(query)
        return web.Response(body={'data': data})


class CompanyView(BaseView):
    TABLE = Company.__table__

    @property
    def company_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> web.Response:
        query = self.TABLE.select().where(
            self.TABLE.c.company_id == self.company_id
        )
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data': data})

    async def put(self) -> web.Response:
        data = await self.request.json()

        query = self.TABLE.update().values(name=data['name']).where(
            self.TABLE.c.company_id == self.company_id
        ).returning(self.TABLE)
        data = await self.postgres.fetchrow(query)

        if data is None:
            raise HTTPNotFound()

        return web.Response(body={'data': data})

    async def delete(self) -> web.Response:
        query = self.TABLE.delete().where(
            self.TABLE.c.company_id == self.company_id
        ).returning(self.TABLE)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()

        return web.Response(status=204)


class EmployeesView(BaseView):
    async def post(self):
        return web.Response(text='Create and return employee')

    async def get(self):
        return web.Response(text='Get employees')


class EmployeeView(BaseView):
    @property
    def employee_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> web.Response:
        return web.Response(text='Get one employee by id %r' % self.employee_id)

    async def put(self) -> web.Response:
        return web.Response(
            text='Update one employee by id %r' % self.employee_id
        )

    async def delete(self) -> web.Response:
        return web.Response(
            text='Delete one employee by id %r' % self.employee_id
        )


class ProductsView(BaseView):
    async def post(self):
        return web.Response(text='Create and return product')

    async def get(self):
        return web.Response(text='Get products')


class ProductView(BaseView):
    @property
    def product_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self):
        return web.Response(text='Get one product by id %r' % self.product_id)

    async def put(self):
        return web.Response(text='Update productby by id %r' % self.product_id)

    async def delete(self):
        return web.Response(text='Delete product by id %r' % self.product_id)


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