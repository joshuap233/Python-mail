import socket

CRLF = '\r\n'

CMD = {
    'USER', 'PASS', 'LIST', 'RETR', 'DELE', 'QUIT',
    'STAT', 'REST', 'TOP', 'UIDL'
}


class POP3:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port))
        self.file = self.sock.makefile('rb')
        self.hello = self._receive()

    def _send(self, cmd):
        self.sock.sendall(f'{cmd}{CRLF}'.encode())

    def _receive(self):
        line = self.file.readline()
        return line

    def hello(self):
        return self._receive()

    def login(self, user, password):
        self._send(f'USER {user}')
        self._receive()
        self._send(f'PASS {password}')
        return self._receive()

    def list(self):
        self._send('LIST')
        return self._receive()

    def retr(self, eid):
        self._send(f'RETR {eid}')

    def connect(self, user, password):
        self.login(user, password)
        self.list()
        self.retr(1)

    def delete(self, eid):
        self._send(f'DELE {eid}')
        return self._receive()

    def quit(self):
        self._send(f'QUIT')
        self.sock.close()

    def data(self):
        for f in self.file:
            print(f)
