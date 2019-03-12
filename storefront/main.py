import argparse
import os
from functools import partial
from types import MappingProxyType
from typing import Mapping

import aioredis
from aiohttp import PAYLOAD_REGISTRY
from aiohttp.web import run_app
from aiohttp.web_app import Application
from asyncpgsa import PG

from storefront.handlers import HANDLERS
from storefront.payloads import JsonPayload


MODULE_PATH = os.path.abspath(os.path.dirname(__file__))

print(os.getenv('STOREFRONT_PORT', 8080))

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, help='Listen host',
                    default=os.getenv('STOREFRONT_HOST', '0.0.0.0'))
parser.add_argument('--port', type=int, help='Listen port',
                    default=os.getenv('STOREFRONT_PORT', 8080))
parser.add_argument('--db-url', type=str, help='Database url',
                    default=os.getenv('STOREFRONT_DB_URL'))
parser.add_argument('--redis-url', type=str, help='Redis url',
                    default=os.getenv('STOREFRONT_REDIS_URL'))


async def setup_db(db_url: str, app: Application):
    pg = PG()
    await pg.init(db_url)
    app['postgres'] = pg


async def setup_redis(redis_url, app: Application):
    app['redis'] = await aioredis.create_redis(redis_url)


def create_app(*, db_url: str, redis_url: str):
    app = Application()

    setup_db_with_url = partial(setup_db, db_url)
    app.on_startup.append(setup_db_with_url)

    setup_redis_with_url = partial(setup_redis, redis_url)
    app.on_startup.append(setup_redis_with_url)

    for handler in HANDLERS:
        app.router.add_route('*', handler.URL_PATH, handler)

    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return app


def main():
    args = parser.parse_args()

    if not args.db_url:
        parser.error('Please specify database url (--db-url)')
        exit(1)

    if not args.redis_url:
        parser.error('Please specify redis url (--redis-url)')
        exit(1)

    app = create_app(db_url=str(args.db_url),
                     redis_url=str(args.redis_url))

    run_app(app, host=args.host, port=args.port)
