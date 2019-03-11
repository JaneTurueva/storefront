from http import HTTPStatus

from sqlalchemy.engine import Connection
from storefront.models import Company, Employee, Product


async def test_products_get(app_client, temp_db_conn: Connection):
    # Создаем компанию
    query = Company.__table__.insert().values(name='test_company').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(name='Vasy', company_id=company['company_id']).returning(
        Employee.__table__
    )
    employee = temp_db_conn.execute(query).fetchone()

    # Создаем продукты в базе
    query = Product.__table__.insert().values([
        {'name': 'moloko',
        'employee_id': employee['employee_id'],
        'price': 1},
       {'name': 'salo',
        'employee_id': employee['employee_id'],
        'price': 5}]).returning(Product.__table__)

    # Сохраняем их в dict по product_id
    products = {
        row['product_id']: row
        for row in temp_db_conn.execute(query).fetchall()
    }

    # Получаем товары из API
    resp = await app_client.get('/products')

    assert resp.status == 200
    data = await resp.json()
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], list)

    # Проверяем ответ
    for received_product in data['data']:
        product = products[received_product['product_id']]
        assert product['name'] == received_product['name']
        assert product['employee_id'] == received_product['employee_id']
        assert float(product['price']) == received_product['price']


async def test_products_post(app_client, temp_db_conn):
    # Создаем компанию
    query = Company.__table__.insert().values(name='test_company').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем сотрудника в базе
    query = Employee.__table__.insert().values(name='Vasy', company_id=company['company_id']).returning(
        Employee.__table__
    )
    employee = temp_db_conn.execute(query).fetchone()

    # Создаем продукт через API
    resp = await app_client.post('/products', data={
        'name': 'moloko',
        'employee_id': employee['employee_id'],
        'price': 5
    })

    # Проверяем ответ
    assert resp.status == HTTPStatus.CREATED
    data = await resp.json()
    assert isinstance(data, dict)
    assert 'data' in data
    assert isinstance(data['data'], dict)
    assert data['data']['name'] == 'moloko'
    assert data['data']['employee_id'] == employee['employee_id']
    assert data['data']['price'] == 5.