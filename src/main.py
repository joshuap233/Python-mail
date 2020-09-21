import socket
from base64 import b64encode, b64decode
from typing import Union

from src.Message import Message

CRLF = '\r\n'


class Socket(socket.socket):
    def sendall_data(self, data: Union[str, Message]):
        if not data.endswith(CRLF):
            data = data + CRLF
        self.sendall(data.encode())


class Mail:
    CMD = {
        'HELO', 'MAIL FROM:', 'RCPT TO:',
        'DATA', 'REST', 'VRFY', 'EXPN',
        'NOOP', 'QUIT', 'AUTH'
    }

    def __init__(self, host, port, password, user):
        self.HOST = host
        self.PORT = port
        self.PASSWORD = password
        self.USER = user
        self.sock = None

    @staticmethod
    def _toBs64(data):
        return b64encode(data.encode()).decode()

    def receive(self, base64: bool = False):
        recv = self.sock.recv(1024).decode()
        if base64:
            recv = b64decode(recv[4:])
        print(recv)

    def connect(self) -> Socket:
        self.sock = Socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((self.HOST, self.PORT))

        # connect 后220, helo 后250, auth login 后 334
        self.sock.sendall_data(CRLF.join([f'HELO {socket.gethostname()}', 'AUTH LOGIN']))
        self.receive()

        # send user后334, send PASSWORD 后235
        self.sock.sendall_data(CRLF.join([self._toBs64(self.USER), self._toBs64(self.PASSWORD)]))
        self.receive()
        self.receive()

        return self.sock

    def send(self, to: str, msg: Message) -> None:
        # mail from 后 250,RCPT TO后250, DATA后354
        # 发送请求头与请求体后250
        self.sock.sendall_data(CRLF.join([f'MAIL From: <{self.USER}>', 'RCPT TO: <shu@shushugo.com>', 'DATA']))
        self.receive()

        msg.headers.update({
            'From': self.USER,
            'To': to,
        })

        self.sock.sendall_data(msg)
        self.receive()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.sendall_data('QUIT')
        self.sock.close()
