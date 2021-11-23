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
