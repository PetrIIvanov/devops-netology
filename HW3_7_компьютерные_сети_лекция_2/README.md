<h1>Домашнее задание 3.7. Компьютерные сети, лекция 2 - Петр Иванов</h1>

<h3>1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?</h3>

Windows: IPCONFIG
Linux: ip link

<h3>2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?</h3>

Используется протокол arp. Есть две программки для этого = arp и arp-scan. Они показывают кто ещё есть в сегменте. 

<h3>3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.</h3>

Виртуальные сети (VLAN)

Пакет vlan ( с vconfig) говорит, что его лучше не использовать 

	vagrant@vagrant:~$ vconfig --help
	Warning: vconfig is deprecated and might be removed in the future, please migrate to ip(route2) as soon as possible!
	
Поэтому так
	~~~
	vagrant@vagrant:~$ sudo ip link add link eth0 name eth0.700 type vlan id 700
	vagrant@vagrant:~$ ip -details link
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
		link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 minmtu 0 maxmtu 0 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
	2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
		link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 46 maxmtu 16110 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
	3: eth0.700@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
		link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 0 maxmtu 65535
		vlan protocol 802.1Q id 700 <REORDER_HDR> addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
	vagrant@vagrant:~$ sudo ip addr add 10.100.10.77/24 dev eth0.700
	vagrant@vagrant:~$ sudo ip link set dev eth0.700 up
	~~~
	
Чтобы изменения были постоянными нужно редактировать /etc/network/interfaces

	# add vlan 700 on eth0 - static IP address
	auto eth0.700
	iface eth0.700 inet static
		  address 10.100.10.77
		  netmask 255.255.255.0
		  pre-up sysctl -w net.ipv6.conf.eth0/700.disable_ipv6=1
		  

И ещё нужно отредактировать /etc/modules, чтобы включить модуль 802 при загрузке. 

<h3>4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.</h3>

Типы есть LACP - открытый стандарт и всякие частные собственные стандарты у Cisco, например. 

Типы балансировки  (mode) указаны тут: https://www.kernel.org/doc/Documentation/networking/bonding.txt
Нет смысла их перепечатывать.  


Пример конфига (с сайта Ubuntu)

	# eth0 is manually configured, and slave to the "bond0" bonded NIC
	auto eth0
	iface eth0 inet manual
		bond-master bond0
		bond-primary eth0

	# eth1 ditto, thus creating a 2-link bond.
	auto eth1
	iface eth1 inet manual
		bond-master bond0

	# bond0 is the bonding NIC and can be used like any other normal NIC.
	# bond0 is configured using static network information.
	auto bond0
	iface bond0 inet static
		address 192.168.1.10
		gateway 192.168.1.1
		netmask 255.255.255.0
		bond-mode active-backup
		bond-miimon 100
		bond-slaves none

Или такой:
	# The primary network interface
	auto bond0
	iface bond0 inet static
		address 192.168.1.150
		netmask 255.255.255.0	
		gateway 192.168.1.1
		dns-nameservers 192.168.1.1 8.8.8.8
		dns-search domain.local
			slaves eth0 eth1
			bond_mode 0
			bond-miimon 100
			bond_downdelay 200
			bond_updelay 200

<h3>5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.</h3>

- 2^(32-29=3) = 8 адресов. Из них доступных для присваивания 6
- 2^ (29-24=5) = 32 сетки
- 10.10.10.0/29,10.10.10.8/29, 10.10.10.16/29


<h3>6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. 
Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.</h3>

Можно использовать 100.64.0.0/26

<h3>7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?</h3>

И там и там команда arp. 

показать таблицу:
	Windows: arp -a 
	Linux: arp -n

Удалить кеш:
	Windows: arp -d (под админом) или netsh interface ip delete arpcache (тоже под админом) 
	Linux: sudo ip -s -s neigh flush all
	
Удалить один:
	Windows: arp -d 172.25.54.102 (под админом)
	Linux: sudo arp -d 10.0.2.3



