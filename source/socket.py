import json
import socket
from time import sleep
from typing import Tuple, Union
from source.kernel import KernelGame


class Client:
    server_addr = '127.0.0.1'
    server_port = 20202

    def __init__(self, kernel:KernelGame) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not self.tryServer(): return
        if not self.startConnection(): return
    
    def tryServer(self) -> bool:
        responce = self.sock.connect_ex((self.server_addr, self.server_port))
        if responce==0: return True
        else: return False
    
    def startConnection(self) -> bool:
        try:
            self.sock.connect((self.server_addr, self.server_port))
        except Exception as e:
            return False #FIXME aggiungi log
        else:
            return True

    def stopConnection(self) -> None:
        self.sock.close()
        self.kernel.endConnection()

    def checkedLoop(self) -> None:
        while self.sock.connect_ex((self.server_addr, self.server_port))==0:
            sleep(10)
        self.kernel.endConnection()

    def send(self, *args:str) -> None:
        try:
            msg = args[0]
            for el in args[1:]:
                msg += '||'+el
            msg = msg.encode('utf-8')
            self.sock.send(msg)
        except Exception as e:
            pass

    def recv(self) -> Tuple[int, str, Union[str, tuple, dict, None]]:
        try:
            msg = self.sock.recv(4096)
            msg = msg.decode('utf-8')
            status, type, msg = msg.split('||', 2)
            status = int(status)
            if type=='str':
                msg = msg
            elif type=='tuple':
                msg = tuple(msg.split('||'))
            elif type=='dict':
                msg = json.loads(msg)
            else:
                msg = None
            return (status, type, msg)
        except Exception as e:
            pass