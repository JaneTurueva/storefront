from http import HTTPStatus

from jsonschema import validate
from sqlalchemy.engine import Connection

from storefront.handlers import CompaniesView
from storefront.models import Company
from tests.schemas import (
    COMPANIES_LIST_RESPONSE_SCHEMA, COMPANY_RESPONSE_SCHEMA
)


async def test_companies_get(app_client, temp_db_conn: Connection,
                             redis_client):
    # Очистить кэш
    await redis_client.execute('del', CompaniesView.CACHE_KEY)

    # Создаем несколько компаний в базе
    companies = [{'name': 'test one'}, {'name': 'test two'}]
    query = Company.__table__.insert().values(companies).returning(
        Company.__table__
    )
    # Сохраняем их в dict по company_id
    rows = {
        row['company_id']: row
        for row in temp_db_conn.execute(query).fetchall()
    }

    # Получаем компании из базы
    resp = await app_client.get('/companies')

    assert resp.status == 200
    data = await resp.json()
    validate(data, COMPANIES_LIST_RESPONSE_SCHEMA)

    # Сверяем имена каждой полученной компании
    for received_company in data['data']:
        row = rows[received_company['company_id']]
        assert row['name'] == received_company['name']


async def test_companies_post(app_client):
    # Создаем компанию через API
    resp = await app_client.post('/companies', data={
        'name': 'Example company'
    })

    # Проверяем ответ
    assert resp.status == HTTPStatus.CREATED
    data = await resp.json()
    validate(data, COMPANY_RESPONSE_SCHEMA)
    assert data['data']['name'] == 'Example company'
