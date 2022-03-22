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
  
  
~~~MYSQL
+------+-----------+--------------+---------+
| User | Host      | Full Name    | Comment |
+------+-----------+--------------+---------+
| test | localhost | James Pretty | NULL    |
+------+-----------+--------------+---------+
1 row in set (0.01 sec)
~~~

## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.
  
~~~MYSQL
SELECT TABLE_NAME,
	   ENGINE
FROM   information_schema.TABLES
WHERE  TABLE_SCHEMA = 'test_db';

--->> InnoDB

~~~
  
 
Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
- на `InnoDB`
  
~~~MYSQL
|        5 | 0.05234425 | ALTER TABLE test_db.orders ENGINE=MyISAM
|        6 | 0.07052575 | ALTER TABLE test_db.orders ENGINE=InnoDB
~~~


~~~MYSQL
SELECT  QUERY_ID, SUM(DURATION) FROM information_schema.PROFILING WHERE QUERY_ID in (5,6) GROUP BY QUERY_ID ORDER BY 1;
+----------+---------------+
| QUERY_ID | SUM(DURATION) |
+----------+---------------+
|        5 |      0.052348 |
|        6 |      0.070529 |
+----------+---------------+
2 rows in set, 1 warning (0.00 sec)
~~~

## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных 
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб 
- Буффер кеширования 30% от ОЗУ 
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.

~~~
innodb_log_buffer_size         = 1M
innodb_buffer_pool_size        = 256M
innodb_file_per_table          = 1
innodb_file_format             = Barracuda
innodb_flush_method            = O_DSYNC
innodb_flush_log_at_trx_commit = 2
innodb_log_file_size           = 100M
~~~

---