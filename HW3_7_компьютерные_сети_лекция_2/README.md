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
	
	
Чтобы изменения были постоянными нужно редактировать /etc/network/interfaces

	# add vlan 700 on eth0 - static IP address
	auto eth0.700
	iface eth0.700 inet static
		  address 10.100.10.77
		  netmask 255.255.255.0
		  pre-up sysctl -w net.ipv6.conf.eth0/700.disable_ipv6=1
		  

<h3>4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.</h3>
