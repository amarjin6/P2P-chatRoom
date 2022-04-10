import socket
import threading
import sys
import os
import time
from datetime import datetime

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
* /help - Show how this message
* /hooray - Beautiful greeting message
* /history - Request history from members
@Created by Alexander Marjin@
'''

HOORAY = '''
Lorem Ipsum is simply dummy text of the printing and typesetting industry.
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
when an unknown printer took a galley of type and scrambled it to make a type specimen book.
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently
with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
'''


def greeting():
    print(GREETING)


def usage():
    print(USAGE)
    os._exit(0)


def create():
    '''
    Creates a socket object
    :return: socket, username, empty dictionary
    '''
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
    '''
    Connects to all online members
    :param: s: current socket
    :param: name: current name
    '''
    while True:
        s.sendto(f'__join{name}'.encode('utf-8'), ('255.255.255.255', PORT))


def check(s: socket.socket, members: dict):
    '''
    Checks whether there is still connected members
    :param: s: current socket
    :param: members: dictionary with connected members
    '''
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
    '''
    Listens and analyze sent messages
    :param s: current socket
    :param members: dictionary with connected members
    '''
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

        elif msg_text[:6] != '__join' and msg_text[:8] == '/members':
            print('All active members:')
            for addr in list(members.keys()):
                print(f'{members[addr]}: {addr[0]}')
            continue

        elif msg_text[:6] != '__join' and msg_text[:8] != '/members' and msg_text[:5] == '/help':
            print(f'{members[addr]}: {GREETING}')
            continue

        elif msg_text[:6] != '__join' and msg_text[:8] != '/members' and msg_text[:5] != '/help' and msg_text[
                                                                                                     :7] == '/hooray':
            print(f'{members[addr]}: {HOORAY}')
            continue

        elif msg_text[:6] != '__join' and msg_text[:8] != '/members' and msg_text[:5] != '/help' and msg_text[
                                                                                                     :7] != '/hooray':
            now = datetime.now()
            print(f'{now.strftime("%H:%M:%S")} {members[addr]}: {msg_text}')
            continue


def send(s: socket.socket, members: dict):
    '''
    Sends message to all members
    :param s: current socket
    :param members: dictionary with connected members
    :return:
    '''
    while True:
        ss = input('')
        for addr in list(members.keys()):
            s.sendto(ss.encode('utf-8'), addr)


def main():
    s, name, members = create()
    greeting()
    # Create threads
    t1 = threading.Thread(target=connect, args=(s, name))
    t2 = threading.Thread(target=listen, args=(s, members))
    t3 = threading.Thread(target=check, args=(s, members))
    t4 = threading.Thread(target=send, args=(s, members))

    # Start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()


if __name__ == '__main__':
    main()
