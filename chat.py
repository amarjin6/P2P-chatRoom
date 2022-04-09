import socket
import threading

UDP_SIZE = 65535  # UDP protocol maximus

DEFAULT_IP = '127.0.0.1'  # Default listening IP

DEFAULT_PORT = 8000  # Default listening port

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


def listen(host: str = DEFAULT_IP, port: int = DEFAULT_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket object on UDP connection
    s.bind((host, port))
    members = {}
    while True:
        msg, addr = s.recvfrom(UDP_SIZE)

        if not msg:
            continue

        msg_text = msg.decode('utf-8')
        if msg_text[:6] == '__join' and addr not in members:
            members[addr] = msg[6:].decode()
            for addr in members.keys():
                s.sendto(f'{msg[6:].decode()} joined chat'.encode('utf-8'), addr)
            continue


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP = input('Enter IP:')
    port = int(input('Enter port:'))
    name = input('Enter name:')
    s.bind((IP, port))
    sendto = (DEFAULT_IP, DEFAULT_PORT)
    s.sendto(f'__join{name}'.encode('utf-8'), sendto)
    while True:
        msg, addr = s.recvfrom(UDP_SIZE)

        if not msg:
            continue

        msg_text = msg.decode('utf-8')
        print(msg_text)


if __name__ == '__main__':
    greeting()
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=connect)
    t1.start()
    t2.start()
