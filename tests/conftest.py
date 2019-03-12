import os

import aioredis
import pytest
from alembic.command import upgrade as upgrade_command
from sqlalchemy import create_engine

from storefront.main import create_app
from storefront.utils import database, get_alembic_config


DB_URL = os.getenv('CI_DB_URL',
                   'postgresql://api:hackme@0.0.0.0:5432/storefront')
REDIS_URL = os.getenv('CI_REDIS_URL', 'redis://localhost')


@pytest.fixture()
def temp_db():
    """
    Создает временную базу и прогоняет миграции.
    Возвращает url для подключения к временной базе данных.
    """
    with database(DB_URL) as db_url:
        config = get_alembic_config(db_url)
        upgrade_command(config, 'head')
        yield db_url


@pytest.fixture()
def temp_db_conn(temp_db):
    """
    Возвращает объект Connection sqlalchemy к временной базе данных.
    """
    engine = create_engine(temp_db)
    with engine.connect() as conn:
        yield conn


@pytest.fixture()
async def redis_client():
    """
    Возвращает подключенного клиента к redis.
    """
    redis = await aioredis.create_redis(REDIS_URL)
    yield redis


@pytest.fixture()
def app(temp_db: str):
    """
    Создает aiohttp приложение.
    """
    app = create_app(
        db_url=temp_db,
        redis_url=REDIS_URL
    )
    yield app


@pytest.fixture()
async def app_client(app, aiohttp_client):
    """
    Создает клиента для обращений к aiohttp приложению.
    """
    client = await aiohttp_client(app)
    yield client
