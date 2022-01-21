import socket


if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 54321))
    while True:
        sock.send(str(input('>>> ')).encode('utf-8'))
        print(sock.recv(1024).decode('utf-8'))