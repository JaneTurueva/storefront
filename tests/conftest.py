import pytest
from alembic.command import upgrade as upgrade_command
from sqlalchemy import create_engine

from storefront.main import create_app
from storefront.utils import database, get_alembic_config


@pytest.fixture()
def temp_db():
    with database('postgresql://api:hackme@0.0.0.0:5432/storefront') as db_url:
        config = get_alembic_config(db_url)
        upgrade_command(config, 'head')
        yield db_url


@pytest.fixture()
def temp_db_conn(temp_db):
    engine = create_engine(temp_db)
    with engine.connect() as conn:
        yield conn


@pytest.fixture()
def app(temp_db: str):
    app = create_app(temp_db)
    yield app


@pytest.fixture()
async def app_client(app, aiohttp_client):
    client = await aiohttp_client(app)
    yield client