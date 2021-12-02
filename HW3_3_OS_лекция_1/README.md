<h1>Домашнее задание 3.3. Операционные системы, лекция 1 - Петр Иванов</h1>

<h3>1. Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, это shell builtin, поэтому запустить strace непосредственно на cd не получится. Тем не менее, вы можете запустить strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. Вам нужно найти тот единственный, который относится именно к cd. Обратите внимание, что strace выдаёт результат своей работы в поток stderr, а не в stdout.</h3>

	chdir("/tmp") # вот этот системный вызов работает
	
<h3>2. Попробуйте использовать команду file на объекты разных типов на файловой системе</h3>

Например 

	vagrant@netology1:~$ file /dev/tty
	/dev/tty: character special (5/0)
	vagrant@netology1:~$ file /dev/sda
	/dev/sda: block special (8/0)
	vagrant@netology1:~$ file /bin/bash
	/bin/bash: ELF 64-bit LSB shared object, x86-64
	
Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.
   
   
	Сначала он ищет в текущей папке /home/vagrant/.magic.mgc /home/vagrant/.magic, 
	потом пробует /etc/magic.mgc (эти три не найдены) и финально находит /etc/magic

<h3>3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).</h3>

	$ > /proc/[PID]/fd/[FID]  #$ > /proc/123/fd/321
	но проблему это решит только временно, приложение продолжит туда писать. И рано или поздно всё придётся повторить. 
	к тому же если приложение использует lseek, то оно всё равно может обвалиться, если не обрабатывает возврат -1
	

<h3>4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?</h3>	

	Нет, не занимают. Они уже завершились, просто родитель не запросил их статус. 
	Поэтому они просто занимают место в табличке процессов и ID.

<h3>5. В iovisor BCC есть утилита opensnoop:

	root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
	/usr/sbin/opensnoop-bpfcc
	
На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.</h3>

	Команда
	strace -f 2>&1 bash 'dpkg -L bpfcc-tools | grep sbin/opensnoop' | grep openat
	

	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libtinfo.so.6", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/dev/tty", O_RDWR|O_NONBLOCK) = 3
	openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
	
	Команда 
	sudo strace -f 2>&1 1>/dev/null /usr/sbin/opensnoop-bpfcc | grep openat | less
	
	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libutil.so.1", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libexpat.so.1", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
	openat(AT_FDCWD, "/usr/bin/pyvenv.cfg", O_RDONLY) = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/usr/pyvenv.cfg", O_RDONLY) = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/etc/localtime", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/encodings/__pycache__/__init__.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/codecs.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/encodings", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/encodings/__pycache__/aliases.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/encodings/__pycache__/utf_8.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/encodings/__pycache__/latin_1.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/io.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/abc.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/site.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/os.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/stat.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/_collections_abc.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/posixpath.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/genericpath.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	openat(AT_FDCWD, "/usr/lib/python3.8/__pycache__/_sitebuiltins.cpython-38.pyc", O_RDONLY|O_CLOEXEC) = 3
	
но это не конец. 

<h3>6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.</h3>

	использует одноимённый системный вызов uname 
	
строчка из man
	
	Part of the utsname information is also accessible via
    /proc/sys/kernel/{ostype, hostname, osrelease, version,
	domainname}.
	
<h3>7. Чем отличается последовательность команд через ; и через && в bash? Например:

	root@netology1:~# test -d /tmp/some_dir; echo Hi
	Hi
	root@netology1:~# test -d /tmp/some_dir && echo Hi
	root@netology1:~#

Есть ли смысл использовать в bash &&, если применить set -e?
</h3>

	&& запустит команду справа тогда и только тогда, когда первая завершилась ок. 
	; запустит команду справа в любом случае
	
	смысл использовать есть, чтобы явно подчеркнуть важное поведение команды. 
	однажды где-то что-то не проставится, или кусок кода скопируешь этот, 
	а он работать не будет и ты не будешь знать почему, а может и не ты даже. 

	а так, если использовать set -e, то bash остановится при первом же провале. 
	в том числе и при && 
	
<h3></h3>
	