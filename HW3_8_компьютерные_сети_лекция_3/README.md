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

<h3></h3>	
