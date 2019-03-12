from http import HTTPStatus

from jsonschema import validate
from sqlalchemy.engine import Connection
from storefront.models import Company, Employee
from tests.schemas import EMPLOYEE_RESPONSE_SCHEMA


async def test_employee_get(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(
        name='test', company_id=company['company_id']).returning(
        Employee.__table__
    )
    employee = temp_db_conn.execute(query).fetchone()

    # Получаем сотрудника через API
    resp = await app_client.get('/employees/%d' % employee['employee_id'])
    assert resp.status == HTTPStatus.OK
    data = await resp.json()

    # Проверяем полученные данные
    validate(data, EMPLOYEE_RESPONSE_SCHEMA)
    assert employee['company_id'] == data['data']['company_id']
    assert employee['name'] == data['data']['name']


async def test_employee_get_404(app_client):
    resp = await app_client.get('/employees/999')
    assert resp.status == HTTPStatus.NOT_FOUND


async def test_employee_put(app_client, temp_db_conn):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(
        name='test', company_id=company['company_id']).returning(
        Employee.__table__
    )
    employee = temp_db_conn.execute(query).fetchone()

    # Меняем компанию через API
    resp = await app_client.put('/employees/%d' % employee['employee_id'],
                                data={'name': 'New name',
                                      'company_id': company['company_id']})

    # Проверяем ответ
    assert resp.status == HTTPStatus.OK
    data = await resp.json()
    validate(data, EMPLOYEE_RESPONSE_SCHEMA)
    assert data['data']['name'] == 'New name'
    assert data['data']['company_id'] == company['company_id']


async def test_employee_put_404(app_client):
    resp = await app_client.put('/employees/999', data={'name': 'New name',
                                                        'company_id': 1212})
    assert resp.status == HTTPStatus.NOT_FOUND


async def test_employee_put_400(app_client):
    resp = await app_client.put('/employees/999', data={'unknown': 'value'})
    assert resp.status == HTTPStatus.BAD_REQUEST


async def test_employee_delete(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(
        name='test', company_id=company['company_id']).returning(
        Employee.__table__
    )
    employee = temp_db_conn.execute(query).fetchone()

    # Удаляем сотрудника через API
    resp = await app_client.delete('/employees/%d' % employee['employee_id'])
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_employee_delete_404(app_client):
    resp = await app_client.delete('/employees/999')
    assert resp.status == HTTPStatus.NOT_FOUND
