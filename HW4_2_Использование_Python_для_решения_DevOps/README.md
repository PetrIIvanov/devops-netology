<h1>Домашнее задание 4.2. Использование Python для решения типовых DevOps задач - Петр Иванов</h1>

<h3>1. Есть скрипт:

	#!/usr/bin/env python3
	a = 1
	b = '2'
	c = a + b
	
	Какое значение будет присвоено переменной c?
	Как получить для переменной c значение 12?
	Как получить для переменной c значение 3?

</h3>

Какое значение будет присвоено переменной c? Будет ошибка: 

	----> 3 c = a + b  

	TypeError: unsupported operand type(s) for +: 'int' and 'str'
	
Как получить для переменной c значение 12?

	с = 3 * 4 #(шутка)
	c = str(a) + str(b) # строка '12'

Как получить для переменной c значение 3?

	c = int(a) + int(b) # число 3

<h3>2. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. 
Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, 
относительно локальных изменений. Этим скриптом недовольно начальство, потому 
что в его выводе есть не все изменённые файлы, а также непонятен полный путь к 
директории, где они находятся. Как можно доработать скрипт ниже, чтобы он 
исполнял требования вашего руководителя?</h3>	

~~~python3
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
~~~

<h3>3. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий 
в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём 
как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу 
этого скрипта в директориях, которые не являются локальными репозиториями.</h3>

Скрипт с доработками:

~~~python3
#!/usr/bin/env python3

import os
import sys, getopt

#print(sys.argv)
def usage():
    print('Usage: python script.py -p "/path_to/git_enabled/directory"')


def process_args(argv):
    work_path = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:v", ["help", "path="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-p", "--path"):
            work_path = a
        else:
            assert False, "unhandled option"

    return work_path

def main():
    #print(sys.argv)

    if len(sys.argv) == 1:
        usage()
        sys.exit(2)

    work_path = process_args(sys.argv[1:])

    print ('Project directory: ' + work_path)

    bash_command = ['[ -d "' + work_path + '" ]',"cd " + work_path, "git status -s"]
    result_os = os.popen(' && '.join(bash_command)).read()

    #check if exists
    if len(result_os) == 0:
        print(work_path + ' is not a directory or not existing.')

    #check if git enabled
    if result_os.find('not a git repository') != -1:
        print (work_path + ' is not a git repository')
        sys.exit()

    #process output
    for result in result_os.split('\n'):
        try:
            if result[1] == 'M':
                prepare_result = 'Modified: ' + result[3:]
                print(prepare_result)

            elif result[1] == '?':
                prepare_result = 'Untracked: ' + result[3:]
                print(prepare_result)
        except:
            next

    sys.exit()

    return 0 # для красоты и порядку

if __name__ == "__main__":
    main()
~~~


<h3>4. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, 
что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, 
где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто 
меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за 
собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали 
в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать 
скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод 
в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего 
IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом 
в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.   

Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com. </h3>

Скрипт:

~~~python3
#!/usr/bin/env python3

import socket

def check_host(host_name):

    ip = ''
    old_ip = ''
    last_ip = ''

    filename = host_name + '_ip.log'

    try:
        with open(filename,'r') as history:
            old_ip = history.read()
    except Exception as e:
        #print('No history for ' + host_name + ' existing yet')
        pass


    if len(old_ip) > 8:
        last_ip = old_ip.split('\n')[-2]
        # [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>
        # <URL сервиса> - <его IP>


        #print('Last ip was: ' + last_ip)



    try:
        ip = socket.gethostbyname(host_name)

        if (last_ip != ip) & (len(last_ip) > 0):
            print('[ERROR] '+ host_name + ' IP mismatch: ' + last_ip + ' ' + ip)
        else:
            print(host_name + ' - ' + ip)

        with open(filename, 'a') as out:
            out.write(ip + '\n')
    except Exception as e:
        #print('Opps, ' + host_name + 'feels bad today')
        #print(e)
        pass

    return

def main():

    #print (socket.gethostbyname('google.com'))
    hosts_to_control = ['drive.google.com', 'mail.google.com', 'google.com']

    for host in hosts_to_control:
        check_host(host)

    return 0

if __name__ == "__main__":
    main()
~~~

Тесты: 

	vagrant@vagrant:~$ rm *_ip.log
	vagrant@vagrant:~$ python3 control_ip.py
	drive.google.com - 64.233.163.194
	mail.google.com - 216.58.209.197
	google.com - 216.58.210.142
	vagrant@vagrant:~$ echo "ffffffffffff" > google.com_ip.log
	vagrant@vagrant:~$ python3 control_ip.py
	drive.google.com - 64.233.163.194
	mail.google.com - 216.58.209.197
	[ERROR] google.com IP mismatch: ffffffffffff 216.58.209.174

