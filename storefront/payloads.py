import json
from datetime import datetime
from functools import singledispatch
from types import MappingProxyType
from typing import Any, Callable
from uuid import UUID

from aiohttp.payload import JsonPayload as _JsonPayload
from asyncpg import Record
from decimal import Decimal


@singledispatch
def convert(value):
    raise NotImplementedError(f'Unserializable value: {value!r}')


@convert.register(Record)
def convert_asyncpg_record(value: Record):
    return dict(value)


@convert.register(datetime)
def convert_datetime(value: datetime):
    return value.isoformat()


@convert.register(UUID)
def convert_uuid(value: UUID):
    return str(value)

@convert.register(Decimal)
def convert_decimal(value: Decimal):
    return float(value)

@convert.register(MappingProxyType)
def convert_mapping_proxy_type(value: MappingProxyType):
    return dict(value.items())


class JsonPayload(_JsonPayload):
    def __init__(self, value, dumps: Callable[[Any], str] = None, **kwargs):
        if dumps is not None:
            self._dumps = dumps
        super().__init__(value, dumps=self._dumps, **kwargs)

    @staticmethod
    def _dumps(value):
        return json.dumps(value, default=convert)


__all__ = (
    'JsonPayload',
)