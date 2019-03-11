from http import HTTPStatus

from sqlalchemy.engine import Connection
from storefront.models import (
    Company, Employee, Product, EmployeeProductRelation
)


async def test_employee_products_get(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(
        name='test', company_id=company['company_id']
    ).returning(Employee.__table__)
    employee = temp_db_conn.execute(query).fetchone()

    # Создаем продукт
    query = Product.__table__.insert().values(
        name='Moloko', price=2.0
    ).returning(Product.__table__)
    product = temp_db_conn.execute(query).fetchone()

    # Создаем связь между сотруником и продуктом
    query = EmployeeProductRelation.__table__.insert().values(
        employee_id=employee['employee_id'],
        product_id=product['product_id']
    ).returning(EmployeeProductRelation.__table__)
    temp_db_conn.execute(query).fetchone()

    # Получаем сотрудника через API
    resp = await app_client.get('/employees/%d/products' % employee['employee_id'])
    assert resp.status == HTTPStatus.OK

    data = await resp.json()
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], list)
    assert len(data['data']) == 1

    # Проверяем полученные данные
    assert product['product_id'] == data['data'][0]['product_id']
    assert product['name'] == data['data'][0]['name']
    assert float(product['price']) == data['data'][0]['price']


async def test_employee_products_post(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(
        name='test', company_id=company['company_id']
    ).returning(Employee.__table__)
    employee = temp_db_conn.execute(query).fetchone()

    # Создаем продукт
    query = Product.__table__.insert().values(
        name='Moloko', price=2.0
    ).returning(Product.__table__)
    product = temp_db_conn.execute(query).fetchone()

    # Создаем связь сотруника с продуктом через API
    resp = await app_client.post(
        '/employees/%d/products' % employee['employee_id'],
        data={'product_id': product['product_id']}
    )
    assert resp.status == HTTPStatus.CREATED

    data = await resp.json()
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], dict)

    # Проверяем полученные данные
    assert product['product_id'] == data['data']['product_id']
    assert product['name'] == data['data']['name']
    assert float(product['price']) == data['data']['price']


async def test_employee_products_delete(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(
        name='test', company_id=company['company_id']
    ).returning(Employee.__table__)
    employee = temp_db_conn.execute(query).fetchone()

    # Создаем продукт
    query = Product.__table__.insert().values(
        name='Moloko', price=2.0
    ).returning(Product.__table__)
    product = temp_db_conn.execute(query).fetchone()

    # Создаем связь между сотруником и продуктом
    query = EmployeeProductRelation.__table__.insert().values(
        employee_id=employee['employee_id'],
        product_id=product['product_id']
    ).returning(EmployeeProductRelation.__table__)
    temp_db_conn.execute(query).fetchone()

    # Удаляем связь через API
    resp = await app_client.delete('/employees/%d/products/%d' % (
        employee['employee_id'], product['product_id']
    ))
    assert resp.status == HTTPStatus.NO_CONTENT
