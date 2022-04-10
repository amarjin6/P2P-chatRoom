import socket
import threading
import sys
import os
import time

UDP_SIZE = 65535  # UDP protocol maximus

PORT = 8000  # Default listening port

OFFSET = 2  # Offset for checking connection

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
Here are some tips for YOU:
* /members - Show all connected members
* /history - Request history from members
* /hooray - Beautiful greeting message
@Created by Alexander Marjin@
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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows several applications to listen the socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # indicates that packets will be broadcast
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
            time.sleep(10)
            m = []
            try:
                for i in range(len(list(members.keys())) + OFFSET):
                    msg, addr1 = s.recvfrom(UDP_SIZE)
                    msg_text = msg.decode('utf-8')
                    m.append(msg_text)

            except ConnectionResetError:
                continue

            f = False
            for msg_text in m:
                if msg_text[:6] == '__join' and members[addr] == msg_text[6:]:
                    f = True
                    continue

            if not f:
                print(f'{members[addr]} left chat')
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

        elif msg_text[:6] != '__join':
            print(f'{members[addr]}: {msg_text}')
            continue


def send(s: socket.socket, members: dict):
    while True:
        ss = input('')
        for addr in list(members.keys()):
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
