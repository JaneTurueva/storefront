from http import HTTPStatus

from sqlalchemy.engine import Connection
from storefront.models import Company, Product


async def test_product_get(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем продукт
    query = Product.__table__.insert().values(name='moloko', price=5).returning(
        Product.__table__
    )
    product = temp_db_conn.execute(query).fetchone()

    # Получаем продукт через API
    resp = await app_client.get('/products/%d' % product['product_id'])
    assert resp.status == HTTPStatus.OK
    data = await resp.json()

    # Проверяем полученные данные
    assert product['name'] == data['data']['name']
    assert float(product['price']) == data['data']['price']


async def test_product_get_404(app_client):
    resp = await app_client.get('/products/999')
    assert resp.status == HTTPStatus.NOT_FOUND


async def test_product_put(app_client, temp_db_conn):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем продукт
    query = Product.__table__.insert().values(name='moloko', price=5).returning(
        Product.__table__
    )
    product = temp_db_conn.execute(query).fetchone()

    # Меняем продукт через API
    resp = await app_client.put('/products/%d' % product['product_id'],
                                data={'name': 'New name', 'price': 10.})

    # Проверяем ответ
    assert resp.status == HTTPStatus.OK
    data = await resp.json()
    assert data['data']['name'] == 'New name'
    assert data['data']['price'] == 10.


async def test_product_put_404(app_client):
    resp = await app_client.put('/products/999', data={
        'name': 'New name', 'price': 2.
    })
    assert resp.status == HTTPStatus.NOT_FOUND


async def test_product_put_400(app_client):
    resp = await app_client.put('/products/999', data={'unknown': 'value'})
    assert resp.status == HTTPStatus.BAD_REQUEST


async def test_product_delete(app_client, temp_db_conn: Connection):
    # Создаем компанию в базе
    query = Company.__table__.insert().values(name='test').returning(
        Company.__table__
    )
    company = temp_db_conn.execute(query).fetchone()

    # Создаем продукт
    query = Product.__table__.insert().values(name='moloko', price=5).returning(
        Product.__table__
    )
    product = temp_db_conn.execute(query).fetchone()

    # Удаляем продукт через API
    resp = await app_client.delete('/products/%d' % product['product_id'])
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_product_delete_404(app_client):
    resp = await app_client.delete('/products/999')
    assert resp.status == HTTPStatus.NOT_FOUND