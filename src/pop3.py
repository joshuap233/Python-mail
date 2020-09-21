import socket

CRLF = '\r\n'


class Socket(socket.socket):
    def sendall_data(self, data):
        if not data.endswith(CRLF):
            data = data + CRLF
        self.sendall(data.encode())


sock = Socket(socket.AF_INET, socket.SOCK_STREAM)


def receive():
    recv = sock.recv(1024)
    print(recv)


def pop3(host, port, user, password):
    sock.connect((host, port))
    receive()

    sock.sendall_data(f'USER {user}')
    receive()

    sock.sendall_data(f'PASS {password}')
    receive()

    sock.sendall_data('LIST')
    receive()

    sock.sendall_data('RETR 1')
    receive()

    sock.sendall_data('DELE 1')
    receive()

    sock.sendall_data('QUIT')
    receive()

    sock.close()
