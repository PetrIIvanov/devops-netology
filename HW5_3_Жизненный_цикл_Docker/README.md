<h1>"5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера" - Петр Иванов</h1>

## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

## Решение 1

Файл манифеста

	~~~docker
	#home work :: TEST
	FROM nginx:1.21.6

	#change default page
	COPY ./custom.html /usr/share/nginx/html/index.html
	~~~

ссылка на контейнер:	
https://hub.docker.com/repository/docker/blackskif/netologynginx

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.


## Решение 3

Команды и вывод

	  107  docker run -it --rm -d -p 8081:80 --name d_centos --mount type=bind,source="$(pwd)"/Data,target=/Data centos
	  111  docker run -it --rm -d -p 8082:80 --name d_debian --mount type=bind,source="$(pwd)"/Data,target=/Data debian
	  112  docker ps
	  113  docker exec d_centos ls /Data
	  114  docker exec d_centos touch /Data/created_from_centos.txt
	  116  touch ./Data/created_from_host.txt
	  117  docker exec d_debian ls /Data
	  118  history

	vagrant@vagrant:~$ docker exec d_debian ls /Data
	created_from_centos.txt
	created_from_host.txt
