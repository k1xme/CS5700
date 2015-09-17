
#!/usr/bin/python
import ssl
import socket
import sys


SSL_ENABLE = False
PORT = 27993
SSL_PORT = 27994
HEAD = 'cs5700%s2015 '
HELLO_MSG = 'HELLO %s\n'
SOLUTION_MSG = '%d\n'
ERROR_MSG = 'Unknown_Husky_ID'
FLAG_START_POS = len(HEAD)


'''
The command of launching this app:

    $ ./client <-p port> <-s> [hostname] [NEU ID]

'''


def main():
    global HEAD
    global HELLO_MSG
    global SOLUTION_MSG
    global ERROR_MSG
    global FLAG_START_POS
    global SSL_PORT, PORT
    global SSL_ENABLE

    if len(sys.argv) < 3:
        print "Not enough argument\n"
        return
    
    if '-t' in sys.argv: HEAD = HEAD % 'spring'
    else: HEAD = HEAD % 'f'

    host = sys.argv[-2]
    HELLO_MSG = HEAD + (HELLO_MSG % sys.argv[-1])

    if '-s' in sys.argv:
        SSL_ENABLE = True
        PORT = SSL_PORT
    
    if '-p' in sys.argv: PORT = sys.argv[2]

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if SSL_ENABLE: my_socket = ssl.wrap_socket(my_socket)

    try:
        my_socket.connect((host, PORT))
    except Exception, e:
        raise e

    my_socket.sendall(HELLO_MSG)

    while True:

        msg = my_socket.recv(1024)

        if ERROR_MSG in msg:
            print ERROR_MSG
            return
        
        if "BYE" in msg:
            print msg[FLAG_START_POS:FLAG_START_POS+64]
            return
        print msg
        num1, op, num2 = msg.split()[-3:]
        sol = 0
        if op == "+": sol = int(num1) + int(num2)
        elif op == "-": sol = int(num1) - int(num2)
        elif op == "*": sol = int(num1) * int(num2)
        else: sol = int(num1) / int(num2)

        my_socket.sendall(HEAD + SOLUTION_MSG % sol)



if __name__ == '__main__':
    main()