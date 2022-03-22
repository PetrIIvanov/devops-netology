<h1>"6.3. MySQL" - Петр Иванов</h1>

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.

Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

	~~~
	mysql> status
	--------------
	mysql  Ver 8.0.28 for Linux on x86_64 (MySQL Community Server - GPL)
	Server version:         8.0.28 MySQL Community Server - GPL

	~~~

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

	~~~
	Ответ: 1
	~~~

В следующих заданиях мы будем продолжать работу с данным контейнером.


## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

	~~~MYSQL
	CREATE USER 'test'@'localhost'
	  IDENTIFIED WITH mysql_native_password BY 'test-pass'
	  WITH MAX_QUERIES_PER_HOUR 100 
	  PASSWORD EXPIRE INTERVAL 180 DAY
	  FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2  
	  ATTRIBUTE '{"fname": "James", "lname": "Pretty"}';
	~~~


Предоставьте привилегии пользователю `test` на операции SELECT базы `test_db`.
	~~~MYSQL
	GRANT SELECT ON test_db.* TO 'test'@'localhost';
	~~~

    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.

	~~~MYSQL
	SELECT
	USER AS User,
	HOST AS Host,
	CONCAT(ATTRIBUTE->>"$.fname"," ",ATTRIBUTE->>"$.lname") AS 'Full Name',
	ATTRIBUTE->>"$.comment" AS Comment
	FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
	WHERE USER='test' AND HOST='localhost';
	~~~
Output:
	~~~
	+------+-----------+--------------+---------+
	| User | Host      | Full Name    | Comment |
	+------+-----------+--------------+---------+
	| test | localhost | James Pretty | NULL    |
	+------+-----------+--------------+---------+
	1 row in set (0.01 sec)
	~~~
