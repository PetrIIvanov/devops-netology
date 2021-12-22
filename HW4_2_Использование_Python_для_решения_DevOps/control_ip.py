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
