import socket
import threading
import sys

UDP_SIZE = 65535  # UDP protocol maximus

TCP_SIZE = 16384  # TCP protocol size (max = 65535)

PORT = 8000  # Default listening port

MEMBERS_AMOUNT = 10  # The number of participants to which the server will simultaneously listen (max = inf)

USAGE = '''
[?] How to use [?]
python chat.py [host] [username]
(?) Examples (?)
python chat.py 127.0.0.1 Alex
python chat.py 127.0.0.2 Tim
python chat.py 127.0.0.3 John
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
    sys.exit()


def create_udp():
    '''
    Creates a socket object
    :return: socket, username, empty dictionary
    '''

    if len(sys.argv) != 3:
        usage()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows several applications to listen the socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # indicates that packets will be broadcast
    except socket.error as e:
        print(f'Failed to create UDP socket: {e}')
        sys.exit()

    IP = sys.argv[1]
    name = sys.argv[2]
    members = {}
    try:
        s.bind((IP, PORT))
    except socket.error as e:
        print(f'Failed connection to host: {e}')
        sys.exit()
    return s, name, members, IP


def create_tcp(ip: str):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows several applications to listen the socket
    except socket.error as e:
        print(f'Failed to create TCP socket: {e}')
        sys.exit()

    try:
        s.bind((ip, PORT))
    except socket.error as e:
        print(f'Failed connection to host: {e}')
        sys.exit()

    return s


def connect(s: socket.socket, name: str):
    '''
    Connects to all online members
    :param: s: current socket
    :param: name: current name
    '''

    while True:
        try:
            s.sendto(f'__join{name}'.encode('utf-8'), ('255.255.255.255', PORT))
        except KeyboardInterrupt:
            print('Bye!')
            sys.exit()


def listen_udp(s: socket.socket, members: dict):
    while True:
        try:
            msg, addr = s.recvfrom(UDP_SIZE)
        except ConnectionResetError:
            continue

        except KeyboardInterrupt:
            print('Bye!')
            sys.exit()

        if not msg:
            continue

        msg_text = msg.decode('utf-8')
        if msg_text[:6] == '__join' and addr not in members:
            members[addr] = msg[6:].decode()
            print(f'{msg[6:].decode()} joined chat')
            continue


def listen_tcp(s: socket.socket, members: dict):
    '''
    Listens and analyze sent messages
    :param s: current socket
    :param members: dictionary with connected members
    '''

    while True:
        try:
            s.listen(MEMBERS_AMOUNT)
            conn, addr = s.accept()
            data = conn.recv(16384)
            udata = data.decode("utf-8")
            print("Data: " + udata)

        except KeyboardInterrupt:
            print('Bye!')
            sys.exit()


def send(s: socket.socket, members: dict):
    '''
    Sends message tщ all members
    :param ip: source IP
    :param s: current socket
    :param members: dictionary with connected members
    :return:
    '''
    while True:
        try:
            ss = input('')
            for addr in list(members.keys()):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect(addr)
                s.send(ss.encode('utf-8'))
                s.shutdown(1)
                s.close()

        except KeyboardInterrupt:
            print('Bye!')
            sys.exit()


def main():
    # Create socket with its tools
    s, name, members, IP = create_udp()
    sock = create_tcp(IP)
    greeting()

    # Create threads
    t1 = threading.Thread(target=connect, args=(s, name))
    t2 = threading.Thread(target=listen_udp, args=(s, members))
    t3 = threading.Thread(target=listen_tcp, args=(sock, members))
    t4 = threading.Thread(target=send, args=(sock, members), daemon=True)

    # Start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()


if __name__ == '__main__':
    main()
