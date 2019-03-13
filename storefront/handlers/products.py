from http import HTTPStatus

from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest
from aiohttp.web_response import Response
from aiohttp_validate import validate
from asyncpg import ForeignKeyViolationError

from storefront.handlers.base import BaseView
from storefront.models import Product


class ProductsView(BaseView):
    URL_PATH = '/products'

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'price': {'type': 'number'}
            },
            'required': ['name', 'price'],
            'additionalProperties': False
        }
    )
    async def post(self, data, request) -> Response:
        query = Product.__table__.insert().values(data).returning(
            Product.__table__
        )
        data = await self.postgres.fetchrow(query)
        return Response(body={'data': data}, status=HTTPStatus.CREATED)

    async def get(self) -> Response:
        query = Product.__table__.select()
        data = await self.postgres.fetch(query)
        return Response(body={'data': data})


class ProductView(BaseView):
    URL_PATH = '/products/{id}'

    @property
    def product_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> Response:
        query = Product.__table__.select().where(
            Product.__table__.c.product_id == self.product_id
        )
        data = await self.postgres.fetchrow(query)

        if data is None:
            raise HTTPNotFound()
        return Response(body={'data': data})

    @validate(
        request_schema={
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'price': {'type': 'number'}
            },
            'required': ['name', 'price'],
            'additionalProperties': False
        },
        response_schema={
            'type': 'object',
            'data': {'type': 'object'},
            'required': ['data'],
            'additionalProperties': False
        }
    )
    async def put(self, data, request) -> Response:
        query = Product.__table__.update().values(data).where(
            Product.__table__.c.product_id == self.product_id
        ).returning(Product.__table__)
        data = await self.postgres.fetchrow(query)

        if data is None:
            raise HTTPNotFound()

        return Response(body={'data': data})

    async def delete(self) -> Response:
        try:
            query = Product.__table__.delete().where(
                Product.__table__.c.product_id == self.product_id
            ).returning(Product.__table__)
            data = await self.postgres.fetchrow(query)

            if data is None:
                raise HTTPNotFound()
        except ForeignKeyViolationError:
            raise HTTPBadRequest(text=('Product has relations with employees '
                                       'and can not be deleted'))

        return Response(status=204)
