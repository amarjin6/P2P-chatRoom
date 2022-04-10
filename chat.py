import socket
import threading

UDP_SIZE = 65535  # UDP protocol maximus

DEFAULT_IP = '127.0.0.1'  # Default listening IP

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


def greeting():
    print('Welcome to chat!')


def usage():
    print(USAGE)


members = {}


def listen():
    while True:
        msg, addr = s.recvfrom(UDP_SIZE)

        if not msg:
            continue

        msg_text = msg.decode('utf-8')
        if msg_text[:6] == '__join' and addr not in members:
            members[addr] = msg[6:].decode()
            for addr in members.keys():
                print(f'{msg[6:].decode()} joined chat')
            continue

        elif msg_text[:6] != '__join':
            print(msg_text)
            continue


def connect():
    while True:
        s.sendto(f'__join{name}'.encode('utf-8'), ('255.255.255.255', PORT))


def create():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    IP = input('Enter IP:')
    name = input('Enter name:')
    s.bind((IP, PORT))
    return s, name


def send():
    while True:
        ss = input('')
        for addr in members.keys():
            s.sendto(f'{name}: {ss}'.encode('utf-8'), addr)


if __name__ == '__main__':
    greeting()
    s, name = create()
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=connect)
    t3 = threading.Thread(target=send)
    t1.start()
    t2.start()
    t3.start()
