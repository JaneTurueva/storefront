Storefront
**********

API витрины магазина. Позволяет наполнять витрину магазина товарами, а также
назначать для товаров ответственных сотрудников.

.. contents:: **Содержание**
   :depth: 2


Как запустить
=============

.. code-block:: shell

   # Смигрировать базу данных
   docker run -it --rm \
      --env STOREFRONT_DB_URL=postgresql://api:hackme@HOST:5432/storefront \
      janeturueva/storefront \
      storefront-db upgrade head

   # Запустить контейнер
   docker run -d --rm -p8080:8080 \
      --env STOREFRONT_HOST=0.0.0.0 \
      --env STOREFRONT_PORT=8080 \
      --env STOREFRONT_DB_URL=postgresql://api:hackme@${DB_HOST}:5432/storefront \
      --env STOREFRONT_REDIS_URL=redis://${REDIS_HOST} \
      janeturueva/storefront


Как использовать (HTTP API)
===========================

Компании
--------

**Создать компанию**

.. code-block:: shell

   curl --header "Content-Type: application/json" --request POST \
      --data '{"name":"ООО Рога и Копыта"}' \
      http://localhost:8080/companies
   
.. code-block:: json

   {
      "data": {
         "company_id": 1,
         "name": "ООО Рога и Копыта",
         "created_at": "2019-03-13T20:11:58.150475+00:00",
         "updated_at": "2019-03-13T20:11:58.150483+00:00"
      }
   }
    
Сотрудники
----------

**Добавить сотрудника компании**

.. code-block:: shell

   curl --header "Content-Type: application/json" --request POST \
      --data '{"name":"Василий Пупкин", "company_id": 1}' \
      http://localhost:8080/employees

.. code-block:: json
   
   {
      "data": {
         "employee_id": 1,
         "name": "Василий Пупкин 1 ",
         "company_id": 1,
         "created_at": "2019-03-13T20:15:03.125603+00:00",
         "updated_at": "2019-03-13T20:15:03.125611+00:00"
      }
   }
   
   
Товары
------

**Добавить товар на витрину**

.. code-block:: shell
   
   curl --header "Content-Type: application/json" --request POST \
      --data '{"name":"Молоко", "price": 10.00}' \
      http://localhost:8080/products

.. code-block:: json

   {
      "data": {
         "product_id": 1,
         "name": "Молоко",
         "price": 10,
         "created_at": "2019-03-13T20:17:20.869164+00:00",
         "updated_at": "2019-03-13T20:17:20.869171+00:00"
      }
   }
   
   
**Получить все товары на витрине**
   
.. code-block:: shell
   
   curl http://localhost:8080/products
   
.. code-block:: shell

   {
      "data": [
         {
            "product_id": 1,
            "name": "Молоко",
            "price": 10,
            "created_at": "2019-03-13T20:17:12.226921+00:00",
            "updated_at": "2019-03-13T20:17:12.226944+00:00"
         }
      ]
   }
   
**Удалить товар с витрины**

.. code-block:: shell
   
   curl --request DELETE http://localhost:8080/products/1

Ответственные сотрудники за товар (многие ко многим)
----------------------------------------------------

**Добавить ответственного сотрудника на товар**

.. code-block:: shell

   curl --header "Content-Type: application/json" --request POST \
         --data '{"product_id": 1}' \
         http://localhost:8080/employees/1/products

.. code-block:: json

   {
      "data": {
         "created_at": "2019-03-13T20:17:12.226921+00:00",
         "name": "Молоко",
         "price": 10.0,
         "product_id": 1,
         "updated_at": "2019-03-13T20:17:12.226944+00:00"
      }
   }
   
**Получить список товаров, за которые сотрудник несет ответственность**

.. code-block:: shell

   curl http://localhost:8080/employees/1/products
   
.. code-block:: shell

   {
      "data": [
         {
            "product_id": 1,
            "name": "Молоко",
            "price": 10,
            "created_at": "2019-03-13T20:17:12.226921+00:00",
            "updated_at": "2019-03-13T20:17:12.226944+00:00"
         }
      ]
   }
   
**Снять ответственность сотрудника за товар**

.. code-block:: shell

   curl --request DELETE http://localhost:8080/employees/1/products/1

Как разрабатывать
=================
.. code-block:: shell

   # Склонировать репозиторий
   git clone git@github.com:JaneTurueva/storefront.git
   cd storefront

   # Создать окружение и установить все зависимости
   make devenv

   # Активировать виртуальное окружение
   source env/bin/activate

   # Смигрировать базу данных
   storefront-db upgrade head

   # Создать докер image
   make build

Как тестировать
===============
Для тестирования потребуется postgresql сервер с правами на создание и удаление
баз данных: для каждого теста будет создана отдельная база данных, запущены миграции,
а после того как тест будет закончен база будет удалена.

Тесты проверяют функционал API, а также структуру возвращаемых данных с помощью
jsonschema (не в handlers, чтобы не тратить лишнее время на обработку запросов
в production в aiohttp-validate декораторе).

.. code-block:: shell

   # Запустит py.test, pylama
   export DB_URL=postgresql://api:hackme@0.0.0.0:5432/storefront
   export REDIS_URL=redis://localhost
   make test
