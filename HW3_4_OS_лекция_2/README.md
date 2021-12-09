<h1>Домашнее задание 3.4. Операционные системы, лекция 2 - Петр Иванов</h1>

<h3>1. На лекции мы познакомились с node_exporter. В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter:

	- поместите его в автозагрузку
	- предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на systemctl cat cron)
	- удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.
	
</h3>

Done  

	EnvironmentFile у crone не работает видимо 
	
	vagrant@vagrant:~$ cat /etc/default/cron
	# This file has been deprecated. Please add custom options for cron using
	# $ systemctl edit cron.service
	# or
	# $ systemctl edit --full cron.service
  

Настройки сервиса у меня
	[Unit]
	Description=Node Exporter
	After=network.target
	Documentation=https://github.com/prometheus/node_exporter

	[Service]
	User=node_exporter
	Group=node_exporter
	Type=simple
	EnvironmentFile=/etc/default/node_exporter
	ExecStart=/usr/local/bin/node_exporter $OPTIONS
	Restart=on-failure
	RestartSec=5


	[Install]
	WantedBy=multi-user.target 

	

<h3>2. Ознакомьтесь с опциями node_exporter и выводом /metrics по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.</h3>

	Команда
	$ curl http://localhost:9100/metrics | grep filesystem (или что надо)
	
	диск: свободное место и ошибки, сколько процессы ждут диск (node_filesystem_avail_bytes, node_filesystem_device_error,node_procs_blocked)
	CPU: сколько процессы ждут процессор node_pressure_cpu_waiting_seconds_total и сколько выполняются  node_schedstat_running_seconds_total 
	память: сколько свободно node_memory_MemFree_bytes 
	
	
<h3>3. Установите в свою виртуальную машину Netdata. Воспользуйтесь готовыми пакетами для установки (sudo apt install -y netdata). После успешной установки:

	в конфигурационном файле /etc/netdata/netdata.conf в секции [web] замените значение с localhost на bind to = 0.0.0.0,
	добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте vagrant reload:
	config.vm.network "forwarded_port", guest: 19999, host: 19999
После успешной перезагрузки в браузере на своем ПК (не в виртуальной машине) вы должны суметь зайти на localhost:19999. 
Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.</h3>

	Всё получилось, только после перезагрузки машина не хотела по SSH пускать. Перегрузил вместе с Windows. потом заработало как часы. 
	
<h3>4. Можно ли по выводу dmesg понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?</h3>

	Конечно можно, там производитель BIOS указывается
	DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006

<h3>5. Как настроен sysctl fs.nr_open на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (ulimit --help)?</h3>

	Это лимит на количество открытых файловых дескрипторов в системе. У меня это 1024*1024 = 1048576
	ulimit -n (количество открытых файлов в shell и его дочках) 
	ulimit -aH показывает теоретически возможные лимиты (ограничен сверху fs.nr_open)
	
<h3>6. Запустите любой долгоживущий процесс (не ls, который отработает мгновенно, а, например, sleep 1h) в отдельном неймспейсе процессов; 
покажите, что ваш процесс работает под PID 1 через nsenter. 
Для простоты работайте в данном задании под root (sudo -i). 
Под обычным пользователем требуются дополнительные опции (--map-root-user) и т.д.</h3>

