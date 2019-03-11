from http import HTTPStatus

from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPBadRequest
from aiohttp.web_response import Response
from aiohttp_validate import validate
from asyncpg import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import select, and_

from storefront.handlers.base import BaseView
from storefront.models import Employee, EmployeeProductRelation, Product


class EmployeesView(BaseView):
    URL_PATH = '/employees'
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
    async def post(self, data, request) -> Response:
        query = Employee.__table__.insert().values(name=data['name'], company_id=data['company_id']).returning(Employee.__table__)
        data = await self.postgres.fetchrow(query)
        return Response(body={'data': data}, status=HTTPStatus.CREATED)

    async def get(self) -> Response:
        query = Employee.__table__.select()
        data = await self.postgres.fetch(query)
        return Response(body={'data': data})


class EmployeeView(BaseView):
    URL_PATH = '/employees/{id}'

    @property
    def employee_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> Response:
        query = Employee.__table__.select().where(Employee.__table__.c.employee_id == self.employee_id)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()
        return Response(body={'data': data})

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
    async def put(self, data, request) -> Response:
        query = Employee.__table__.update().values(
            name=data['name'], company_id=data['company_id']
        ).where(
            Employee.__table__.c.employee_id == self.employee_id
        ).returning(Employee.__table__)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()
        return Response(body={'data': data})

    async def delete(self) -> Response:
        query = Employee.__table__.delete().where(
            Employee.__table__.c.employee_id == self.employee_id).returning(Employee.__table__)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()
        return Response(status=204)



class EmployeeProductsView(BaseView):
    URL_PATH = '/employees/{employee_id}/products'

    @property
    def employee_id(self) -> int:
        return int(self.request.match_info['employee_id'])

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'product_id': {"type": "integer"}
            },
            "required": ["product_id"],
            "additionalProperties": False
        }
    )
    async def post(self, data, request) -> Response:
        async with self.postgres.transaction() as conn:
            try:
                query = EmployeeProductRelation.__table__.insert().values(
                    employee_id=self.employee_id,
                    product_id=data['product_id']
                )
                await conn.fetchrow(query)

                query = Product.__table__.select().where(
                    Product.__table__.c.product_id == data['product_id']
                )
                product = await conn.fetchrow(query)

            except UniqueViolationError:
                raise HTTPConflict()

            except ForeignKeyViolationError:
                raise HTTPBadRequest()

            return Response(body={'data': product}, status=HTTPStatus.CREATED)

    async def get(self) -> Response:
        query = select(Product.__table__.columns).select_from(
            EmployeeProductRelation.__table__.join(
                Product.__table__,
                EmployeeProductRelation.__table__.c.product_id == Product.__table__.c.product_id
            )
        ).where(
            EmployeeProductRelation.__table__.c.employee_id == self.employee_id
        )
        data = await self.postgres.fetch(query)
        return Response(body={'data': data})


class EmployeeProductDeleteView(BaseView):
    URL_PATH = '/employees/{employee_id}/products/{product_id}'

    async def delete(self) -> Response:
        employee_id = int(self.request.match_info['employee_id'])
        product_id = int(self.request.match_info['product_id'])

        query = EmployeeProductRelation.__table__.delete().where(
            EmployeeProductRelation.__table__.c.employee_id == employee_id
        ).where(
            EmployeeProductRelation.__table__.c.product_id == product_id
        ).returning(EmployeeProductRelation.__table__)

        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()

        return Response(status=HTTPStatus.NO_CONTENT)
