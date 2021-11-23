<h1>Домашнее задание 3.1. Работа в терминале, лекция 1 - Петр Иванов</h1>

1. VirtualBox - done
2. Vagrant - done
3. WSL2 работает в windows10 при отключённом Hyper-V параллельно VirtualBox
4. Done
5. Какие ресурсы выделены по-умолчанию?

	- RAM 4GB
	- CPU 2
	- VBoxVGA 4Mb
	- Disk 64Gb
	- Net IntelPRO/1000 MT NAT
 
6. Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: документация. Как добавить оперативной памяти или ресурсов процессора виртуальной машине?

	~~~
	  config.vm.provider "virtualbox" do |vb|
	  #   # Display the VirtualBox GUI when booting the machine
	  #   vb.gui = true
	  #
	  #   # Customize the amount of memory on the VM:
		 vb.memory = "4098"
		 vb.cpus = 4
	  end
	~~~
7. Команда vagrant ssh из директории, в которой содержится Vagrantfile, позволит вам оказаться внутри виртуальной машины без каких-либо дополнительных настроек. Попрактикуйтесь в выполнении обсуждаемых команд в терминале Ubuntu.

	Тут надо сказать, что Ubuntu спросит пароль всё-таки. done.

8. Ознакомиться с разделами man bash, почитать о настройках самого bash:

- какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?

	846 строчка: 
	~~~
	man bash
	HISTFILESIZE
		      The maximum number of lines contained in the history file.  When this variable is assigned a value, the
              history  file  is truncated, if necessary, to contain no more than that number of lines by removing the
              oldest entries.  The history file is also truncated to this size after writing it when a  shell  exits.
              If  the  value is 0, the history file is truncated to zero size.  Non-numeric values and numeric values
              less than zero inhibit truncation.  The shell sets the default value to the  value  of  HISTSIZE  after
              reading any startup files.
	~~~

- что делает директива ignoreboth в bash?

	Параметр управляет логом команд. Туда не попадут команды, начинающиеся с пробела и дубликаты команд.
	
9. В каких сценариях использования применимы скобки {} и на какой строчке man bash это описано?

Когда нужно выполнить список пайплайнов в текущем окруженнии скрипта, должны быть отделены проблами

	257 строчка 
	~~~
       { list; }
              list is simply executed in the current shell environment.  list must be terminated with  a  newline  or
              semicolon.  This is known as a group command.  The return status is the exit status of list.  Note that
              unlike the metacharacters ( and ), { and } are reserved words and must occur where a reserved  word  is
              permitted  to be recognized.  Since they do not cause a word break, they must be separated from list by
              whitespace or another shell metacharacter.
	~~~
10. С учётом ответа на предыдущий вопрос, как создать однократным вызовом touch 100000 файлов? Получится ли аналогичным образом создать 300000? Если нет, то почему?

	можно создавать что-то типа touch {1,2,4,5} или touch 1 2 4 5
	максимальный размер команд лично тут у меня стоит (_POSIX_ARG_MAX) 2 097 152 байт, то получается
	если использовать 0-9, a-z, A-Z 52 символа, log62 (300 000) чуть больше 3, ну пусть 4. 
	Тогда 4х символьными комбинациями мы покроем все файлы, плюс запятые 5 * 300 000 = 1 500 000, меньше лимита
	должно хватить. в циклах я так понимаю уже многократный вызов, поэтому не буду приводить тут скрипт.   
	
11. В man bash поищите по /\[\[. Что делает конструкция [[ -d /tmp ]]

	проверяет, что /tmp существует и это директория, тогда возвращает 1, иначе 0

12. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:

	~~~
	bash is /tmp/new_path_directory/bash
	bash is /usr/local/bin/bash
	bash is /bin/bash
	~~~
	
	Команды  
	
	~~~
	mkdir /tmp/new_path_directory
	cd /tmp/new_path_directory
	cp /bin/bash ./
	PATH="/tmp/new_path_directory:$PATH"
	type -a bash
	~~~
	
13. Чем отличается планирование команд с помощью batch и at?

	at - выполнит команду в определённое время
	batch - выполнит команду, когда нагрузка на машину упадёт ниже limiting load factor, который измеряется в процессорных ядрах. 
	
14. Завершите работу виртуальной машины чтобы не расходовать ресурсы компьютера и/или батарею ноутбука.

	done

