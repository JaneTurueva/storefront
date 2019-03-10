from http import HTTPStatus

from sqlalchemy.engine import Connection
from storefront.models import Company


async def test_companies_get(app_client, temp_db_conn: Connection):
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
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], list)

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
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], dict)
    assert data['data']['name'] == 'Example company'