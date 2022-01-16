<h1>Курсовая работа по итогам модуля "DevOps и системное администрирование" - Петр Иванов</h1>


## Результат

Результатом курсовой работы должны быть снимки экрана или текст:

- Процесс установки и настройки ufw
- Процесс установки и выпуска сертификата с помощью hashicorp vault
- Процесс установки и настройки сервера nginx
- Страница сервера nginx в браузере хоста не содержит предупреждений 
- Скрипт генерации нового сертификата работает (сертификат сервера ngnix должен быть "зеленым")
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)

## Описание проделанной работы

1. Я создал новую машину vagrant (приложить файл)
2. Добавил FW и сконфиругировал его
3. Установил vault (в dev режиме, т.е. в памяти).
4. Выпустил сертификаты для сайта example.com и www.example.com 
	4.1 Добавил первый самоподписанный сертификат в trusted. 
5. Внёс example.com в hosts на VM и хосте как 127.0.0.1
6. Поставил nginx и сконфигурировал на новые сертификаты (скриншот Chrome и wget)
7. Написал скрипт, который генерит новые сертификаты и перезапускает nginx

 
### Процесс установки и настройки ufw
<приложен скриншот 02_ufw_installation.png>

### Процесс установки hashicorp vault
Там всё по сайту ничего интересного 

### Скрипт обновления сертификатов

~~~bash
#!/bin/bash
vault write -format=json pki_int/issue/example-dot-com common_name="www.example.com" ttl="24h" > /etc/vagrant_data/certificates.json
cat /etc/vagrant_data/certificates.json | jq -r '.data.issuing_ca' > /etc/vagrant_data/issue_test.crt
cat /etc/vagrant_data/certificates.json | jq -r '.data.private_key' > /etc/vagrant_data/test.key
cat /etc/vagrant_data/certificates.json | jq -r '.data.certificate' > /etc/vagrant_data/test.crt
cat /etc/vagrant_data/test.crt /etc/vagrant_data/issue_test.crt /etc/vagrant_data/CA_cert_v2.crt > /etc/vagrant_data/ssl_bundle.crt
cp /etc/vagrant_data/ssl_bundle.crt /etc/nginx
cp /etc/vagrant_data/test.key /etc/nginx
systemctl restart nginx
~~~


