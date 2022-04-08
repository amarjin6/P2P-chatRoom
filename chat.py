import socket

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


def usage():
    print(USAGE)


def listen(host: str = DEFAULT_IP, port: int = DEFAULT_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket object on UDP connection
    s.bind((host, port))

    members = []
    while True:
        msg, addr = s.recvfrom(UDP_SIZE)

        if addr not in members:
            members.append(addr)
            # Show message that new Client joined chat

        if not msg:
            continue

        msg_text = msg.decode('utf-8')


if __name__ == '__main__':
    ...
