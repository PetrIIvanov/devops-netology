<h1>Домашнее задание 3.8. Компьютерные сети, лекция 3 - Петр Иванов</h1>

<h3>1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP

	telnet route-views.routeviews.org
	Username: rviews
	show ip route x.x.x.x/32
	show bgp x.x.x.x/32
	
</h3>

	Username: rviews
	route-views>show ip route 89.179.246.148
	Routing entry for 89.178.0.0/15
	  Known via "bgp 6447", distance 20, metric 0
	  Tag 6939, type external
	  Last update from 64.71.137.241 5d10h ago
	  Routing Descriptor Blocks:
	  * 64.71.137.241, from 64.71.137.241, 5d10h ago
		  Route metric is 0, traffic share count is 1
		  AS Hops 3
		  Route tag 6939
		  MPLS label: none


	show bgp - тут очень длинный вывод. 

/32 - ругается 

	route-views>show ip route 89.179.246.148/32
											^
		% Invalid input detected at '^' marker.

<h3>2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации</h3>

Создание
	root@vagrant:/etc/systemd/network# vim /etc/modules (добавляем dummy модуль при старте)
	создаём в 
	/etc/systemd/network/

	10-dummy0.netdev и 10-dummy1.netdev
	---------------
	[NetDev]
	Name=dummy0 (dummy1)
	Kind=dummy
	---------------
	
Конфиг

	# vim /etc/network/interfaces
	-------------------------------------------------------------------
	# interfaces(5) file used by ifup(8) and ifdown(8)
	# Include files from /etc/network/interfaces.d:
	source-directory /etc/network/interfaces.d

	# add vlan 700 on eth0 - static IP address
	auto eth0.700
	iface eth0.700 inet static
		  address 10.100.10.77
		  netmask 255.255.255.0
		  pre-up sysctl -w net.ipv6.conf.eth0/700.disable_ipv6=1

	auto dummy0
	iface dummy0 inet static
		  address 192.168.1.150
		  netmask 255.255.255.0
		  up route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.150

	auto dummy1
	iface dummy1 inet static
		  address 192.168.2.150
		  netmask 255.255.255.0
		  up route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.150

Перезапускаем (dummy можно руками стартовать сначала, потом будет автоматом стартовать)

	#systemctl restart systemd-networkd

Появились
	root@vagrant:/home/vagrant# ip addr | grep "inet "
		inet 127.0.0.1/8 scope host lo
		inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
		inet 10.100.10.77/24 brd 10.100.10.255 scope global eth0.700
		inet 192.168.1.150/24 brd 192.168.1.255 scope global dummy0
		inet 192.168.2.150/24 brd 192.168.2.255 scope global dummy1
