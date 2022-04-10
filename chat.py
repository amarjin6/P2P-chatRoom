import socket
import threading
import sys
import os
import time

UDP_SIZE = 65535  # UDP protocol maximus

PORT = 8000  # Default listening port

USAGE = '''
[?] How to use [?]
python chat.py [host] [username]
(?) Examples (?)
python chat.py 192.168.0.1 Alex
python chat.py 192.168.0.1 Tim
python chat.py 192.168.0.1 John
[?] How to use [?]
'''

GREETING = '''
\u263A Welcome to chat! \u263A
'''


def greeting():
    print(GREETING)


def usage():
    print(USAGE)
    os._exit(0)


def create():
    if len(sys.argv) != 3:
        usage()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    IP = sys.argv[1]
    name = sys.argv[2]
    members = {}
    s.bind((IP, PORT))
    return s, name, members


def connect(s: socket.socket, name: str):
    while True:
        s.sendto(f'__join{name}'.encode('utf-8'), ('255.255.255.255', PORT))


def check(s: socket.socket, members: dict):
    while True:
        for addr in list(members.keys()):
            s.sendto(f'__alive{addr[0]}'.encode('utf-8'), addr)
            time.sleep(15)
            try:
                msg, addr1 = s.recvfrom(UDP_SIZE)
            except ConnectionResetError:
                continue

            if msg.decode('utf-8')[:5] == '__yes':
                print(msg.decode('utf-8'))
                print('OK!')
                continue

            else:
                print(f'{members[addr]} left chat')
                print(msg.decode('utf-8'))
                del members[addr]
                continue


def listen(s: socket.socket, members: dict):
    while True:
        try:
            msg, addr = s.recvfrom(UDP_SIZE)
        except ConnectionResetError:
            continue

        if not msg:
            continue

        msg_text = msg.decode('utf-8')
        if msg_text[:6] == '__join' and addr not in members:
            members[addr] = msg[6:].decode()
            print(f'{msg[6:].decode()} joined chat')
            continue

        elif msg_text[:7] == '__alive':
            sendto = (msg_text[7:], PORT)
            s.sendto(f'__yes{addr[0]}'.encode('utf-8'), sendto)
            continue


        elif msg_text[:6] != '__join' and msg_text[:7] != '__alive' and msg_text[:5] != '__yes':
            print(f'{members[addr]}: {msg_text}')
            continue


def send(s: socket.socket, members: dict):
    while True:
        ss = input('')
        for addr in members.keys():
            s.sendto(ss.encode('utf-8'), addr)


def main():
    s, name, members = create()
    greeting()
    t1 = threading.Thread(target=connect, args=(s, name))
    t2 = threading.Thread(target=listen, args=(s, members))
    t3 = threading.Thread(target=check, args=(s, members))
    t4 = threading.Thread(target=send, args=(s, members))

    t1.start()
    t2.start()
    t3.start()
    t4.start()


if __name__ == '__main__':
    main()
