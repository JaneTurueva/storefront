from http import HTTPStatus

from sqlalchemy.engine import Connection
from storefront.models import Company


async def test_company_get(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    row = temp_db_conn.execute(query).fetchone()

    # Получаем эту компанию через API
    resp = await app_client.get('/companies/%d' % row['company_id'])
    assert resp.status == HTTPStatus.OK
    data = await resp.json()

    # Проверяем полученные данные
    assert row['company_id'] == data['data']['company_id']
    assert row['name'] == data['data']['name']


async def test_company_get_404(app_client):
    resp = await app_client.get('/companies/999')
    assert resp.status == HTTPStatus.NOT_FOUND


async def test_company_put(app_client, temp_db_conn):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    row = temp_db_conn.execute(query).fetchone()

    # Меняем компанию через API
    resp = await app_client.put('/companies/%d' % row['company_id'],
                                data={'name': 'New name'})

    # Проверяем ответ
    assert resp.status == HTTPStatus.OK
    data = await resp.json()
    assert data['data']['name'] == 'New name'
    assert data['data']['company_id'] == row['company_id']


async def test_company_put_404(app_client):
    resp = await app_client.put('/companies/999', data={'name': 'New name'})
    assert resp.status == HTTPStatus.NOT_FOUND


async def test_company_put_400(app_client):
    resp = await app_client.put('/companies/999', data={'unknown': 'value'})
    assert resp.status == HTTPStatus.BAD_REQUEST


async def test_company_delete(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    row = temp_db_conn.execute(query).fetchone()

    # Удаляем эту компанию через API
    resp = await app_client.delete('/companies/%d' % row['company_id'])
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_company_delete_404(app_client):
    resp = await app_client.delete('/companies/999')
    assert resp.status == HTTPStatus.NOT_FOUND