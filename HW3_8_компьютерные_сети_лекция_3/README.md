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
		  post-up route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.150

	auto dummy1
	iface dummy1 inet static
		  address 192.168.2.150
		  netmask 255.255.255.0
		  post-up route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.150

Перезапускаем (dummy можно руками стартовать сначала, потом будет автоматом стартовать)

	#systemctl restart systemd-networkd

Появились
	root@vagrant:/home/vagrant# ip addr | grep "inet "
		inet 127.0.0.1/8 scope host lo
		inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
		inet 10.100.10.77/24 brd 10.100.10.255 scope global eth0.700
		inet 192.168.1.150/24 brd 192.168.1.255 scope global dummy0
		inet 192.168.2.150/24 brd 192.168.2.255 scope global dummy1

Результаты, всё пингуется:

	root@vagrant:/home/vagrant# ping 192.168.1.150
	PING 192.168.1.150 (192.168.1.150) 56(84) bytes of data.
	64 bytes from 192.168.1.150: icmp_seq=1 ttl=64 time=0.025 ms
	64 bytes from 192.168.1.150: icmp_seq=2 ttl=64 time=0.031 ms
	64 bytes from 192.168.1.150: icmp_seq=3 ttl=64 time=0.034 ms
	64 bytes from 192.168.1.150: icmp_seq=4 ttl=64 time=0.031 ms
	64 bytes from 192.168.1.150: icmp_seq=5 ttl=64 time=0.031 ms
	64 bytes from 192.168.1.150: icmp_seq=6 ttl=64 time=0.038 ms
	^C
	--- 192.168.1.150 ping statistics ---
	6 packets transmitted, 6 received, 0% packet loss, time 5129ms
	rtt min/avg/max/mdev = 0.025/0.031/0.038/0.004 ms
	root@vagrant:/home/vagrant# ping 192.168.2.150
	PING 192.168.2.150 (192.168.2.150) 56(84) bytes of data.
	64 bytes from 192.168.2.150: icmp_seq=1 ttl=64 time=0.040 ms
	64 bytes from 192.168.2.150: icmp_seq=2 ttl=64 time=0.031 ms
	^C
	--- 192.168.2.150 ping statistics ---
	2 packets transmitted, 2 received, 0% packet loss, time 1010ms
	
Добавляем маршруты:

	root@vagrant:/home/vagrant# ip route add 172.16.10.0/24 dev dummy0
	root@vagrant:/home/vagrant# ip route add 172.16.11.0/24 dev dummy1 metric 100
	

Смотрим:

	root@vagrant:/home/vagrant# ip route show 172.16.10.0/24
	172.16.10.0/24 dev dummy0 scope link
	root@vagrant:/home/vagrant# ip route show 172.16.11.0/24
	172.16.11.0/24 dev dummy1 scope link metric 100
	root@vagrant:/home/vagrant# ip route show 192.168.1.0/24
	192.168.1.0/24 via 192.168.1.150 dev dummy0 scope link
	192.168.1.0/24 dev dummy0 proto kernel scope link src 192.168.1.150	
	
<h3>3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров</h3>

Вот пример. На машине запущен node_exporter и netdata, которая по нему работает. На порту 22 ssh, systemd-resolve - резолвит локальные адреса. 

	root@vagrant:/home/vagrant# ss -tulpn | grep LISTEN

	tcp    LISTEN   0        4096        127.0.0.53%lo:53             0.0.0.0:*      users:(("systemd-resolve",pid=662,fd=13))
	tcp    LISTEN   0        128               0.0.0.0:22             0.0.0.0:*      users:(("sshd",pid=904,fd=3))
	tcp    LISTEN   0        4096            127.0.0.1:8125           0.0.0.0:*      users:(("netdata",pid=894,fd=62))
	tcp    LISTEN   0        4096              0.0.0.0:19999          0.0.0.0:*      users:(("netdata",pid=894,fd=4))
	tcp    LISTEN   0        4096              0.0.0.0:111            0.0.0.0:*      users:(("rpcbind",pid=661,fd=4),("systemd",pid=1,fd=35))
	tcp    LISTEN   0        128                  [::]:22                [::]:*      users:(("sshd",pid=904,fd=4))
	tcp    LISTEN   0        4096                [::1]:8125              [::]:*      users:(("netdata",pid=894,fd=61))
	tcp    LISTEN   0        4096                    *:9100                 *:*      users:(("node_exporter",pid=895,fd=3))
	tcp    LISTEN   0        4096                 [::]:111               [::]:*      users:(("rpcbind",pid=661,fd=6),("systemd",pid=1,fd=37))
	
<h3>4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?</h3>

	root@vagrant:/home/vagrant# ss -a -u
	State            Recv-Q           Send-Q                      Local Address:Port                       Peer Address:Port          Process
	UNCONN           0                0                               127.0.0.1:8125                            0.0.0.0:*
	UNCONN           0                0                           127.0.0.53%lo:domain                          0.0.0.0:*
	UNCONN           0                0                          10.0.2.15%eth0:bootpc                          0.0.0.0:*
	UNCONN           0                0                                 0.0.0.0:sunrpc                          0.0.0.0:*
	UNCONN           0                0                                   [::1]:8125                               [::]:*
	UNCONN           0                0                                    [::]:sunrpc                             [::]:*

bootpc - это DHCP клиент
https://en.wikipedia.org/wiki/Bootstrap_Protocol

sunrpc - это Sun Remote Procedure call
https://en.wikipedia.org/wiki/Sun_RPC

<h3>5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали.</h3>


= приложить картинку = 