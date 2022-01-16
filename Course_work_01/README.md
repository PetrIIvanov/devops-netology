<h1>Курсовая работа по итогам модуля "DevOps и системное администрирование" - Петр Иванов</h1>


## Результат

Результатом курсовой работы должны быть снимки экрана или текст:

- Процесс установки и настройки ufw
- Процесс установки и выпуска сертификата с помощью hashicorp vault
- Процесс установки и настройки сервера nginx
- Страница сервера nginx в браузере хоста не содержит предупреждений 
- Скрипт генерации нового сертификата работает (сертификат сервера nginx должен быть "зеленым")
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)

## Описание проделанной работы

1. Я создал новую машину vagrant (приложить файл). Порт 4334 хоста проброшен на 443 VM
2. Добавил FW и сконфиругировал его
3. Установил vault (в dev режиме, т.е. в памяти).
4. Выпустил сертификаты для сайта example.com и www.example.com 
	4.1 Добавил первый самоподписанный сертификат в trusted. 
5. Внёс example.com в hosts на VM и хосте как 127.0.0.1
6. Поставил nginx и сконфигурировал на новые сертификаты (скриншот Chrome и wget)
7. Написал скрипт, который генерит новые сертификаты и перезапускает nginx

 
### Процесс установки и настройки ufw
<приложен скриншот 02_ufw_installation.png>

### Процесс установки и выпуска сертификата hashicorp vault
Там всё по сайту ничего интересного, делал как там за исключением последнего шага. Там тоже взял json и потом его разбирал. 

### Скрипт обновления сертификатов
Как выяснилось cron запускает команду с обрезанными переменными окружения, поэтому их нужно экспортировать заново. 

~~~bash
#!/bin/bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root

vault write -format=json pki_int/issue/example-dot-com common_name="www.example.com" ttl="24h" > /etc/vagrant_data/certificates.json
cat /etc/vagrant_data/certificates.json | jq -r '.data.issuing_ca' > /etc/vagrant_data/issue_test.crt
cat /etc/vagrant_data/certificates.json | jq -r '.data.private_key' > /etc/vagrant_data/test.key
cat /etc/vagrant_data/certificates.json | jq -r '.data.certificate' > /etc/vagrant_data/test.crt
cat /etc/vagrant_data/test.crt /etc/vagrant_data/issue_test.crt /etc/vagrant_data/CA_cert_v2.crt > /etc/vagrant_data/ssl_bundle.crt
cp /etc/vagrant_data/ssl_bundle.crt /etc/nginx
cp /etc/vagrant_data/test.key /etc/nginx
systemctl restart nginx && printf "%s %s\n" "$(date)" "new certificate generated successfully" >> /etc/vagrant_data/log.txt  || printf "%s %s\n" "$(date)" "new certificate generation FAILED"  >> /etc/vagrant_data/log.txt

~~~

### Config nginx ("/etc/nginx/sites-available/default")

~~~
server {
        #listen 80 default_server;
        #listen [::]:80 default_server;
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     ssl_bundle.crt;
    ssl_certificate_key test.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;

~~~

### Cron 

crontab -l 
	Запускаем скрипт каждые 2 минуты (для теста, в жизни так не надо)
	
	*/2 * * * * bash /etc/vagrant_data/gen_new_cert_nginx_v2.sh 1>/dev/null 2>&1

  
  
	root@vagrant:~# cat /etc/vagrant_data/log.txt

	Sun 16 Jan 2022 10:40:02 AM UTC new certificate generated successfully
	Sun 16 Jan 2022 10:42:02 AM UTC new certificate generated successfully
	Sun 16 Jan 2022 10:44:01 AM UTC new certificate generated successfully
	Sun 16 Jan 2022 10:46:02 AM UTC new certificate generated successfully
	Sun 16 Jan 2022 10:48:01 AM UTC new certificate generated successfully