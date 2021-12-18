<h1>Домашнее задание 3.6. Компьютерные сети, лекция 1 - Петр Иванов</h1>

<h3>1. Работа c HTTP через телнет.
 - Подключитесь утилитой телнет к сайту stackoverflow.com 
   telnet stackoverflow.com 80
 - отправьте HTTP запрос
	GET /questions HTTP/1.0
	HOST: stackoverflow.com
	[press enter]
	[press enter]
В ответе укажите полученный HTTP код, что он означает?</h3>


Ответ: HTTP/1.1 301 Moved Permanently
Он означает редирект на location: https://stackoverflow.com/questions
Т.е. протокол http больше не поддерживается и подменяется HTTPS


<h3>2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку Network
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку Headers
- укажите в ответе полученный HTTP код.
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
- приложите скриншот консоли браузера в ответ. (не забыть скриншот)
</h3>

Первый ответ 
307 - Internal redirect
Запрос https://stackoverflow.com/ обрабатывался дольше всего


<h3>3. Какой IP адрес у вас в интернете?</h3>

Fixed IP от билайна

<h3>4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой whois</h3>

CORBINA-BROADBAND-STATIC 


<h3>5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой traceroute</h3>

Tracing route to dns.google [8.8.8.8]
over a maximum of 30 hops:

	  1     2 ms    <1 ms    <1 ms  192.168.xxx.xxx 
	  2     2 ms     2 ms     2 ms  78.107.181.110 (CORBINA-MARKORA)
	  3     *        *        *     Request timed out.
	  4     4 ms     3 ms     4 ms  213.234.224.137 (RU-CORBINA-20030523)
	  5     3 ms     3 ms     2 ms  213.234.224.132
	  6     3 ms     3 ms     3 ms  85.21.224.191 (CORBINA-CORE-1-P2P)
	  7     4 ms     4 ms     4 ms  108.170.250.66 ( GOOGLE)
	  8     *       20 ms    19 ms  209.85.255.136  (и дальше там внутри гугловской сети путешествует)
	  9    18 ms    19 ms    19 ms  108.170.235.64
	 10    19 ms    19 ms    19 ms  142.250.56.131
	 11     *        *        *     Request timed out.
	 12     *        *        *     Request timed out.
	 13     *        *        *     Request timed out.
	 14     *        *        *     Request timed out.
	 15     *        *        *     Request timed out.
	 16     *        *        *     Request timed out.
	 17     *        *
	 
<h3>6. Повторите задание 5 в утилите mtr. На каком участке наибольшая задержка - delay?</h3>

На адресе 209.85.255.136 самые большие задержки. Я бы предположил, что это Firewall. 

	Keys:  Help   Display mode   Restart statistics   Order of fields   quit
																				   Packets               Pings
	 Host                                                                        Loss%   Snt   Last   Avg  Best  Wrst StDev
	 1. _gateway                                                                  0.0%    52    0.6   0.6   0.3   1.3   0.2
	 2. 192.168.xx.x                                                              0.0%    52    1.7   2.4   1.7  21.9   2.8
	 3. 78.107.181.110                                                            3.8%    52    3.1   6.7   3.0  57.3   9.7
	 4. (waiting for reply)
	 5. 213.234.224.137                                                           2.0%    51    4.1   4.9   4.0  30.4   3.9
	 6. 213.234.224.132                                                           3.9%    51    4.1   6.2   3.9  69.6   9.9
	 7. 85.21.224.191                                                             0.0%    51    4.3   8.7   4.0  74.9  12.1
	 8. 108.170.250.66                                                            0.0%    51    4.9   8.3   4.6  44.8  10.0
	 9. 209.85.255.136                                                            0.0%    51   20.6  31.3  20.4  97.0  22.4
	10. 108.170.235.64                                                            3.9%    51   19.4  22.0  19.0  52.6   6.2
	11. 142.250.56.131                                                            0.0%    51   19.3  24.0  19.3  61.9  10.6
	12. (waiting for reply)
	13. (waiting for reply)
	14. (waiting for reply)
	15. (waiting for reply)
	16. (waiting for reply)
	17. (waiting for reply)
	18. (waiting for reply)
	19. (waiting for reply)
	20. (waiting for reply)
	21. dns.google                                                               11.8%    51   19.6  20.8  18.5  40.9   4.9

<h3>7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой dig</h3>

	8.8.8.8 primary
	8.8.4.4 secondary

	Записи такие:
	dns.google.com.         900     IN      A       8.8.8.8
	dns.google.com.         900     IN      A       8.8.4.4
	
<h3>8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой dig</h3>

т.е. у них получается прямо от корня DNS есть домен google вместо com и т.п.

	;; ANSWER SECTION:
	8.8.8.8.in-addr.arpa.   3705    IN      PTR     dns.google.

	;; ANSWER SECTION:
	4.4.8.8.in-addr.arpa.   19778   IN      PTR     dns.google.
	

Разница кстати есть, если полное имя использовать или не полное. 
	vagrant@vagrant:~$ ping dns.google.
	PING dns.google (8.8.8.8) 56(84) bytes of data.
	64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=57 time=43.8 ms
	64 bytes from dns.google (8.8.8.8): icmp_seq=2 ttl=57 time=21.2 ms

	vagrant@vagrant:~$ ping dns.google
	PING dns.google (8.8.4.4) 56(84) bytes of data.
	64 bytes from dns.google (8.8.4.4): icmp_seq=1 ttl=105 time=18.5 ms
	64 bytes from dns.google (8.8.4.4): icmp_seq=2 ttl=105 time=72.1 m