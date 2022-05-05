import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 54321))
    message = input('>>> ')
    while message.lower()!='exit':
        sock.send(message.encode('UTF-8'))
        print(sock.recv(1024).decode('UTF-8'))
        message = input('>>> ')