from functools import partial
from types import MappingProxyType
from typing import Mapping

import os

import aioredis
from aiohttp import web, PAYLOAD_REGISTRY
from asyncpgsa import PG
from storefront.handlers import HANDLERS
from storefront.payloads import JsonPayload


MODULE_PATH = os.path.abspath(os.path.dirname(__file__))


async def setup_db(db_url: str, app: web.Application):
    pg = PG()
    await pg.init(db_url)
    app['postgres'] = pg


async def setup_redis(redis_url, app: web.Application):
    app['redis'] = await aioredis.create_redis(redis_url)


def create_app(*, db_url: str, redis_url: str):
    app = web.Application()

    setup_db_with_url = partial(setup_db, db_url)
    app.on_startup.append(setup_db_with_url)

    setup_redis_with_url = partial(setup_redis, redis_url)
    app.on_startup.append(setup_redis_with_url)

    for handler in HANDLERS:
        app.router.add_route('*', handler.URL_PATH, handler)

    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return app


def main():
    app = create_app(
        db_url='postgresql://api:hackme@0.0.0.0:5432/storefront',
        redis_url='redis://localhost'
    )
    web.run_app(app)
