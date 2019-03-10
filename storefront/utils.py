import uuid
from contextlib import contextmanager
from types import SimpleNamespace

import os
from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database
from storefront.main import MODULE_PATH
from yarl import URL


@contextmanager
def database(url: str):
    """
    Создает временнудю базу данных во время вызовы контекст-менеджера и
    удаляет при выходе из него.
    """
    tmp_db_name = '.'.join([uuid.uuid4().hex, 'storefront-ci'])
    tmp_db_url = str(URL(url).with_path(tmp_db_name))

    create_database(tmp_db_url)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)


def get_alembic_config(db_url: str) -> Config:
    cmd_options = SimpleNamespace(
        config=os.path.join(MODULE_PATH, 'alembic.ini'),
        db_url=db_url,
        raiseerr=False,
        rev_range=None,
        verbose=False,
        x=None,
    )

    config = Config(
        file_=cmd_options.config,
        cmd_opts=cmd_options
    )

    config.set_main_option('sqlalchemy.url', db_url)
    config.set_main_option('script_location',
                           os.path.join(MODULE_PATH, 'alembic'))

    return config