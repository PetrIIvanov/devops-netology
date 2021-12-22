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