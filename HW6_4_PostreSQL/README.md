<h1>"6.4. PostgreSQL" - Петр Иванов</h1>

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД  

	\l

- подключения к БД  

	\c

- вывода списка таблиц  

	\dt или \dtS  


- вывода описания содержимого таблиц  

	\d+ pg_roles

- выхода из psql  

	quit



## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

~~~sql
select
	attname
from
	pg_stats
where
	tablename = 'orders'
order by
	avg_width desc
limit 1;

~~~


## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

~~~sql

-- start a transaction
BEGIN;

ALTER TABLE orders rename to orders_old; 

CREATE TABLE public.orders (
	id serial4 NOT NULL,
	title varchar(80) NOT NULL,
	price int4 NULL DEFAULT 0

) partition by range  (price);

CREATE TABLE orders_1 PARTITION of orders
FOR values from (500) TO (MAXVALUE);

CREATE TABLE orders_2 PARTITION of orders
FOR values from (MINVALUE) to (500);

INSERT INTO public.orders
(title, price)
select title, price from orders_old;

DROP TABLE orders_old;

-- commit the change (or roll it back later)
COMMIT;

~~~

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?  

	См. выше

~~~sql
SELECT id, title, price
FROM public.orders_1;


SELECT id, title, price
FROM public.orders_2;

~~~

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

~~~
pg_dump -U postgres -F t test_database > /var/lib/postgresql/backup/hw6_4_test_database_backup.tar
~~~	

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?  

Вот такое добавить
~~~sql
ALTER TABLE orders ADD CONSTRAINT order_title_unique UNIQUE (title);
~~~



