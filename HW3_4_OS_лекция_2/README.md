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

	root@vagrant:~# lsns
			NS TYPE   NPROCS   PID USER            COMMAND
	4026531835 cgroup    127     1 root            /sbin/init
	4026531836 pid       126     1 root            /sbin/init
	4026531837 user      127     1 root            /sbin/init
	4026531838 uts       125     1 root            /sbin/init
	4026531839 ipc       127     1 root            /sbin/init
	4026531840 mnt       115     1 root            /sbin/init
	4026531860 mnt         1    33 root            kdevtmpfs
	4026531992 net       127     1 root            /sbin/init
	4026532162 mnt         1   405 root            /lib/systemd/systemd-udevd
	4026532163 uts         1   405 root            /lib/systemd/systemd-udevd
	4026532164 mnt         1   408 systemd-network /lib/systemd/systemd-networkd
	4026532183 mnt         1   588 systemd-resolve /lib/systemd/systemd-resolved
	4026532184 mnt         4   668 netdata         /usr/sbin/netdata -D
	4026532185 mnt         2  1636 root            unshare -f --pid --mount-proc sleep 1h (вот оно)
	4026532186 pid         1  1637 root            sleep 1h
	4026532249 mnt         1   621 root            /usr/sbin/irqbalance --foreground
	4026532250 mnt         1   633 root            /lib/systemd/systemd-logind
	4026532251 uts         1   633 root            /lib/systemd/systemd-logind
	
  
	root@vagrant:~# nsenter -t 1637 -p -r ps -ef
	UID          PID    PPID  C STIME TTY          TIME CMD
	root           1       0  0 23:21 pts/1    00:00:00 sleep 1h
	root           2       0  0 23:33 pts/1    00:00:00 ps -ef
	
<h3>7. Найдите информацию о том, что такое :(){ :|:& };:. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04
 (это важно, поведение в других ОС не проверялось). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. 
 Вызов dmesg расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число 
 процессов, которое можно создать в сессии?</h3>
	
	[ 3307.972605] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-5.scope
 
	Это определение рекурсивной функции без параметризованного останова. Прекратится когда исчерпается call stack size (ulimit -s)
	у меня это 8мб. Или когда исчерпается количество процессов max user processes (ulimit -u) у меня это 15389. В данном случае параметров нет,
	ставлю на процессы. 
	
	увеличить количество процессов временно можно ulimit -u 64000, аналогично ulimit -s 64000 увеличивает стек. 
	
	