<h1>"6.2. SQL" - Петр Иванов</h1>

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

	~~~
	YML
	
	version: '3.7'
	services:
		postgres:
			image: postgres:12.10
			restart: always
			environment:
			  - POSTGRES_USER=postgres
			  - POSTGRES_PASSWORD=postgres
			logging:
			  options:
				max-size: 10m
				max-file: "3"
			ports:
					- '19999:5432'
			volumes:
			  - ./postgres-data:/var/lib/postgresql/data
			  - ./postgres-backup:/var/lib/postgresql/backup
	~~~
	
## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db
	
	~~~
	см. картинки.
	
	create table if not exists orders  (
	id serial primary key,
	наименование varchar(150),
	цена int);
	
	create table if not exists clients  (
	id serial primary key,
	фамилия varchar(150),
	"страна проживания" varchar(150),
	заказ int,
	   CONSTRAINT fk_order
		  FOREIGN KEY(заказ) 
		  REFERENCES orders(id));

	SELECT grantee, privilege_type,table_name
	FROM information_schema.role_table_grants 
	WHERE grantee not in ('postgres', 'PUBLIC')
	order by 1,3,2
	~~~

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.


	~~~
	
	 INSERT INTO public.orders
	(наименование, цена)
	VALUES('n/a', 0),
	('Шоколад',	10),
	('Принтер',	3000),
	('Книга',	500),
	('Монитор',	7000),
	('Гитара',	4000);
	

	

	INSERT INTO public.clients
	(фамилия, "страна проживания", заказ)
	VALUES
	('Иванов Иван Иванович', 'USA', NULL),
	('Петров Петр Петрович', 	'Canada', NULL),
	('Иоганн Себастьян Бах', 	'Japan', NULL),
	('Ронни Джеймс Дио', 	'Russia', NULL),
	('Ritchie Blackmore', 'Russia', NULL);
	
	select count(1) as qty, 'orders' as _name from public.orders
	union all
	select count(1) as qty, 'clients' as _name  from public.clients;
	~~~

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказк - используйте директиву `UPDATE`.

	~~~
	update clients 
	set заказ  = (select id from orders where наименование like 'Книга')
	where фамилия like 'Иванов Иван Иванович';
	update clients 
	set заказ  = (select id from orders where наименование like 'Монитор')
	where фамилия like 'Петров Петр Петрович';
	update clients 
	set заказ  = (select id from orders where наименование like 'Гитара')
	where фамилия like 'Иоганн Себастьян Бах';


	select фамилия, наименование from clients c 
	inner join orders o 
	on o.id  = c.заказ;
	~~~



## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.  

	~~~
	На картинке там будет join типа hash join - это когда в одной табличке создаются хеши по ключам со списком строк, потом в другой табличке метч идёт по хешу. 
	~~~

	~~~
	explain select фамилия, наименование from clients c 
	inner join orders o 
	on o.id  = c.заказ;
	~~~

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

~~~
Заходим в контейнер
docker exec -it 263f7128629f /bin/bash

Бекапим:
pg_dump -U postgres -F t test_db > /var/lib/postgresql/backup/test_db_backup.tar

Оставнавливаем сервис и запускаем отдельный докер:
docker run --name account-db -e POSTGRES_PASSWORD=secret_password -p 19998:5432 -d --mount type=bind,source="$(pwd)"/postgres-backup,target=/var/lib/postgresql/backup postgres:12.10

Заходим в контейнер
docker exec -it afafc8b5c4de /bin/bash

Восстанавливаем (предварительно надо создать test_db)
pg_restore -U postgres --create --dbname test_db /var/lib/postgresql/backup/test_db_backup.tar

~~~
