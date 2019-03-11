from http import HTTPStatus

from sqlalchemy.engine import Connection
from storefront.models import Company, Employee


async def test_employees_get(app_client, temp_db_conn: Connection):
    # Создаем компанию
    query = Company.__table__.insert().values(name='test_company').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем несколько сотрудников в базе
    employees = [{'name': 'Vasy', 'company_id': company['company_id']},
                 {'name': 'Ben', 'company_id': company['company_id']}]
    query = Employee.__table__.insert().values(employees).returning(
        Employee.__table__
    )
    # Сохраняем их в dict по employee_id
    rows = {
        row['employee_id']: row
        for row in temp_db_conn.execute(query).fetchall()
    }

    # Получаем сотроудников из API
    resp = await app_client.get('/employees')

    assert resp.status == 200
    data = await resp.json()
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], list)

    # Сверяем имя каждого сотрудника и его компанию
    for received_employee in data['data']:
        row = rows[received_employee['employee_id']]
        assert row['name'] == received_employee['name']
        assert row['company_id'] == received_employee['company_id']


async def test_employees_post(app_client, temp_db_conn):
    # Создаем компанию
    query = Company.__table__.insert().values(name='test_company').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника через API
    resp = await app_client.post('/employees', data={
        'name': 'Robert',
        'company_id': company['company_id']
    })

    # Проверяем ответ
    assert resp.status == HTTPStatus.CREATED
    data = await resp.json()
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], dict)
    assert data['data']['name'] == 'Robert'
    assert data['data']['company_id'] == company['company_id']