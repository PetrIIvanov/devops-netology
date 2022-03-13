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