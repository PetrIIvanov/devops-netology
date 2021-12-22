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
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
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

