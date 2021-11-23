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