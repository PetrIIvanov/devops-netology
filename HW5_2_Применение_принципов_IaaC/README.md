<h1>"5.2. Применение принципов IaaC в работе с виртуальными машинами" - Петр Иванов</h1>

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.  

	1. Воспроизвоздимость результатов. Мы можем повторять наши действия 1-в-1
	2. Гарантированное время, деньги и прочие ресурсы. Мы знаем сколько это займёт.
	3. Возможность прогнозировать потребности в ресурсах
	4. Мы можем откатывать изменения в инфраструктуре до стабильных версий. 
	5. Прозрачность и аудирование изменений. Мы знаем, кто точно это сделал и когда. 
	6. Возможность копипастить большие куски архитектуры между разными проектами. 
	7. Возможность гибкого управления инфраструктурой в зависимости от нагрузки 
	
	
- Какой из принципов IaaC является основополагающим?

	Мы пишем инфраструктуру как код и можем получать детерминированный заранее результат. 
	
## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?

	- Работает поверх существующего SSH (не нужен клиент)
	- Много модулей
	- Покрывает все этапы жизненного цикла инфраструктуры
	- на питоне можно много чего дописать, если надо
	
- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

	Мне pull кажется предпочтительным на этапе развёртывания. Когда поднимается много хостов 
	и они могут тянуть конфиги сразу во время старта. По идее это должно происходить быстрее. 
	Источник можно распараллелить и нарастить его производительность. Теоретически при таком 
	сценарии если инфра распадётся физически на две части на время - ничего страшного не произойдёт. 
	С другой стороны обновление в таком сетапе проходят медленнее и есть риск вообще потерять хосты. 
	
	Push хорош на поддержке. Когда надо срочно что-то накатить и не ждать пока клиенты обратятся. 
	Всё быстрее отзывается на изменения. Но тут мы формируем единую точку отказа, которая нам может выйти боком. 
	Если мы каким-то образом "забыли", что у нас есть хост, то мы о нём уже никогда не узнаем.  


## Задача 3

Установить на личный компьютер:

- VirtualBox

	Version 6.1.30 r148432 (Qt5.6.2)
	
- Vagrant

	Vagrant 2.2.19
	
- Ansible

	Тут всё плохо, он на Windows Control Host не ставится. Делать будем как здесь: https://gist.github.com/tknerr/291b765df23845e56a29
	Только CentOS поменяю на Ubuntu, чтобы он не скачивал лишний образ. 
	
	
Поднял 3 хоста на vagrant, node1, node2
	
	~~~vagrant
	Vagrant.configure("2") do |config|

	  config.vm.box = "bento/ubuntu-20.04"

	  config.vm.define "node1" do |machine|
		machine.vm.network "private_network", ip: "172.17.177.21"
		
		
	  end

	  config.vm.define "node2" do |machine|
		machine.vm.network "private_network", ip: "172.17.177.22"
	  end

	  config.vm.define 'controller' do |machine|
		machine.vm.network "private_network", ip: "172.17.177.11"


		  
		machine.vm.provision :ansible_local do |ansible|

		  ansible.playbook       = "test_provision.yml"
		  ansible.verbose        = true
		  ansible.install        = true
		  ansible.limit          = "nodes" # or only "nodes" group, etc. "all"
		  ansible.inventory_path = "inventory_local"
		end
		
	  end

	end
	~~~
	
	
	
	Вывод:
	
	vagrant@vagrant:~$ ansible --version
	ansible [core 2.12.2]
	  config file = /etc/ansible/ansible.cfg
	  configured module search path = ['/home/vagrant/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
	  ansible python module location = /usr/lib/python3/dist-packages/ansible
	  ansible collection location = /home/vagrant/.ansible/collections:/usr/share/ansible/collections
	  executable location = /usr/bin/ansible
	  python version = 3.8.10 (default, Jun  2 2021, 10:49:15) [GCC 9.4.0]
	  jinja version = 2.10.1
	  libyaml = True
	

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*