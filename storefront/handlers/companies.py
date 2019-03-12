import json
from http import HTTPStatus

from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp.web_response import Response
from aiohttp_validate import validate
from asyncpg import UniqueViolationError

from storefront.handlers.base import BaseView
from storefront.models import Company
from storefront.payloads import convert


class CompaniesView(BaseView):
    URL_PATH = '/companies'
    TABLE = Company.__table__

    CACHE_KEY = 'companies-cache'
    CACHE_SECONDS = 60

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
    async def post(self, data, request) -> Response:
        query = self.TABLE.insert().values(name=data['name']).returning(
            self.TABLE
        )
        try:
            data = await self.postgres.fetchrow(query)
        except UniqueViolationError:
            raise HTTPConflict()

        return Response(body={'data': data}, status=HTTPStatus.CREATED)

    async def get(self) -> Response:
        cached = await self.redis.get(self.CACHE_KEY)

        if cached is not None:
            # Есть данные в кэше
            data = json.loads(cached)
        else:
            # Нет данных в кэше, нужно обновить
            query = Company.__table__.select()
            data = await self.postgres.fetch(query)

            cached = json.dumps(data, default=convert)
            await self.redis.setex(
                self.CACHE_KEY,
                self.CACHE_SECONDS * 1000,
                cached
            )

        return Response(body={'data': data})


class CompanyView(BaseView):
    URL_PATH = '/companies/{id}'
    TABLE = Company.__table__

    @property
    def company_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> Response:
        query = self.TABLE.select().where(
            self.TABLE.c.company_id == self.company_id
        )
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()
        return Response(body={'data': data})

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
    async def put(self, data, request) -> Response:

        query = self.TABLE.update().values(name=data['name']).where(
            self.TABLE.c.company_id == self.company_id
        ).returning(self.TABLE)
        data = await self.postgres.fetchrow(query)

        if data is None:
            raise HTTPNotFound()

        return Response(body={'data': data})

    async def delete(self) -> Response:
        query = self.TABLE.delete().where(
            self.TABLE.c.company_id == self.company_id
        ).returning(self.TABLE)
        data = await self.postgres.fetchrow(query)
        if data is None:
            raise HTTPNotFound()

        return Response(status=204)
