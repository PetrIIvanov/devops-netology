<h1>Домашнее задание 3.2. Работа в терминале, лекция 2 - Петр Иванов</h1>

<h3>1. Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.</h3>

Команда cd - внутренняя команда BASH (или другого интерпретатора). На самом деле мы никуда не "переходим", а просто переключаем внутренние указатели в оболочке. Если её реализовывать отдельно, то пришлось бы где-то обмениваться, что куда переключать, как-то это синхронизировать между собой и пр. Проще это никуда наружу не отдавать. 

<h3>2. Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l? man grep поможет в ответе на этот вопрос.</h3>

	~~~
	grep "h1" README.md -c
	~~~

<h3>3. Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?</h3>

	/sbin/init
	
<h3>4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?</h3>
	
	~~~
	ls 2>&1 1>/dev/null | xterm( или другой) 
	upd: ls 2>/dev/pts/1 #(у нас при этом /dev/pts/0)
	~~~

<h3>5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.</h3>

	~~~
	wc -l >test <README.md
	~~~

<h3>6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?</h3>

	~~~
	терминал 1
	$ tty
	/dev/pts/0

	терминал 2
	$ tty
	/dev/pts/1
	
	exec 1>/dev/pts/1 с первого терминала во второй. Данные наблюдать не сможем. Потому что они ушли в другой процесс. 
	~~~

<h3>7. Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?</h3>

Будет создан output дескриптор с ID 5, который будет указывать на текущий STDOUT. Если в него явно вывести, то попадёт всё в STDOUT. 

<h3>8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.</h3>

	создадим файл gen_error.sh
	~~~

	#!/bin/bash
	#test for output streams 

	echo "This Is Error" 1>&2
	echo "This Is Output" 

	~~~
	далее  вот такая конструкция
	~~~
	$ bash 5>&1
	$ bash gen_error.sh 2>&1 >&5 | grep "Error" -c
	This Is Output
	1

	~~~

<h3>9. Что выведет команда cat /proc/$$/environ? Как еще можно получить аналогичный по содержанию вывод?</h3>

	Выведет список текущих переменных. Есть отдельная команда для этого. 
	~~~
	$ printenv
	~~~
	
<h3>10. Используя man, опишите что доступно по адресам /proc/<PID>/cmdline, /proc/<PID>/exe.</h3>

	Первое показывает строку, которой был запущен процесс с аргументами. Второе - это символическая ссылка на исполняемый файл, которым запустили процесс.

	В man такого не нашёл
	~~~
	$ man -wK "proc*cmdline"
	No manual entry for proc*cmdline
	~~~
	
	man proc # Как и написано выше, показывает команду, которой запустили процесс. За исключением процессов-зомби. 
	/proc/[pid]/cmdline
              This read-only file holds the complete command line for the process, unless the process  is  a  zombie.
              In  the  latter case, there is nothing in this file: that is, a read on this file will return 0 charac‐
              ters.  The command-line arguments appear in this file as a set  of  strings  separated  by  null  bytes
              ('\0'), with a further null byte after the last string.
			  
	/proc/[pid]/exe #символическая ссылка на файл, как и ожидалось :)
              Under  Linux 2.2 and later, this file is a symbolic link containing the actual pathname of the executed
              command.  This symbolic link can be dereferenced normally; attempting to open it  will  open  the  exe‐
              cutable.   You  can  even type /proc/[pid]/exe to run another copy of the same executable that is being
              run by process [pid].  If the pathname has been unlinked, the symbolic link  will  contain  the  string
              '(deleted)'  appended  to the original pathname.  In a multithreaded process, the contents of this sym‐
              bolic link are not  available  if  the  main  thread  has  already  terminated  (typically  by  calling
              pthread_exit(3)).

<h3>11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo</h3>

	sse4_2

<h3>12. При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако:

vagrant@netology1:~$ ssh localhost 'tty'
not a tty
Почитайте, почему так происходит, и как изменить поведение.</h3>

	когда мы коннектимся через ssh выделяется по умолчанию pty, tty не цепляется, чтобы облегчить передачу файлов и пр. 
	поправить можно так:

	~~~
	$ ssh -t vagrant@localhost "ssh vagrant@localhost"
	~~~


<h3>13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись reptyr. Например, так можно перенести в screen процесс, который вы запустили по ошибке в обычной SSH-сессии.</h3>

	C top получилось перенести в другой терминал. Однако пришлось помучатся с Ubuntu. 
	echo 0 > /proc/sys/kernel/yama/ptrace_scope # Permission denied
	echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope # работает, помог пп. 14
	
<h3>14. sudo echo string > /root/new_file не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без sudo под вашим пользователем. Для решения данной проблемы можно использовать конструкцию echo string | sudo tee /root/new_file. Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать.</h3>

	> - тут работает текущая оболочка с её контекстом безопасности  
	tee - делает тоже самое, но запускается в контексте sudo с правами админа

 
 