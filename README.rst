Storefront
**********

API витрины магазина. Позволяет наполнять витрину магазина товарами, а также
назначать для товаров ответственных сотрудников.


Как запустить
-------------
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


Как разрабатывать
-----------------
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
---------------
Для тестирования потребуется postgresql сервер с правами на создание и удаление
баз данных.

Для каждого теста будет создана отдельная база данных, запущены миграции,
а после того как тест будет закончен база будет удалена.

Тесты проверяют функционал API, а также структуру возвращаемых данных с помощью
jsonschema (не в handlers, чтобы не тратить лишнее время на обработку запросов
в production в aiohttp-validate декораторе).

.. code-block:: shell

   # Запустит py.test, pylama
   export DB_URL=postgresql://api:hackme@0.0.0.0:5432/storefront
   export REDIS_URL=redis://localhost
   make test
