from http import HTTPStatus

from aiohttp import web
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp_validate import validate
from asyncpg import UniqueViolationError
from asyncpgsa import PG
from storefront.models import Company, Employee, Product


class BaseView(web.View):
    @property
    def postgres(self) -> PG:
        return self.request.app['postgres']


class CompaniesView(BaseView):
    TABLE = Company.__table__

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {"type": "string"},
            },
            "required": ["name"],
            "additionalProperties": False
        }
    )
    async def post(self, data, request) -> web.Response:
        query = self.TABLE.insert().values(name=data['name']).returning(
            self.TABLE
        )
        try:
            data = await self.postgres.fetchrow(query)
        except UniqueViolationError:
            raise HTTPConflict()

        return web.Response(body={'data':data}, status=HTTPStatus.CREATED)

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
        if data is None:
            raise HTTPNotFound()
        return web.Response(body={'data': data})


    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {"type": "string"},
            },
            "required": ["name"],
            "additionalProperties": False
        }
    )
    async def put(self, data, request) -> web.Response:

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

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {"type": "string"},
                'company_id': {"type": "integer"}
            },
            "required": ["name", "company_id"],
            "additionalProperties": False
        }
    )
    async def post(self, data, request):
        query = Employee.__table__.insert().values(name=data['name'], company_id=data['company_id']).returning(Employee.__table__)
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data': data})

    async def get(self):
        query = Employee.__table__.select()
        data = await self.postgres.fetch(query)
        return web.Response(body={'data': data})


class EmployeeView(BaseView):
    @property
    def employee_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> web.Response:
        query = Employee.__table__.select().where(Employee.__table__.c.employee_id == self.employee_id)
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data': data})

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {"type": "string"},
                'company_id': {"type": "integer"}
            },
            "required": ["name", "company_id"],
            "additionalProperties": False
        }
    )
    async def put(self, data, request) -> web.Response:
        query = Employee.__table__.update().values(
            name=data['name'], company_id=data['company_id']
        ).where(
            Employee.__table__.c.employee_id == self.employee_id
        ).returning(Employee.__table__)
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data': data})

    async def delete(self) -> web.Response:
        query = Employee.__table__.delete().where(
            Employee.__table__.c.employee_id == self.employee_id).returning(Employee.__table__)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()
        return web.Response(status=204)


class ProductsView(BaseView):
    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {"type": "string"},
                'employee_id': {"type": "integer"},
                'price': {"type": "number"}
            },
            "required": ["name", "employee_id", "price"],
            "additionalProperties": False
        }
    )
    async def post(self, data, request):
        query = Product.__table__.insert().values(data).returning(Product.__table__)
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data': data})

    async def get(self):
        query = Product.__table__.select()
        data = await self.postgres.fetch(query)
        return web.Response(body={'data': data})


class ProductView(BaseView):
    @property
    def product_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self):
        query = Product.__table__.select().where(Product.__table__.c.product_id == self.product_id)
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data':data})

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {"type": "string"},
                'employee_id': {"type": "integer"},
                'price': {"type": "number"}
            },
            "required": ["name", "employee_id", "price"],
            "additionalProperties": False
        },
        response_schema={
            'type': 'object',
            'data': {'type': 'object'},
            'required': ['data'],
            'additionalProperties': False
        }
    )
    async def put(self, data, request):
        query = Product.__table__.update().values(data).where(Product.__table__.c.product_id == self.product_id).returning(Product.__table__)
        data = await self.postgres.fetchrow(query)
        return web.Response(body={'data': data})

    async def delete(self):
        query = Product.__table__.delete().where(Product.__table__.c.product_id == self.product_id).returning(Product.__table__)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()
        return web.Response(status=204)