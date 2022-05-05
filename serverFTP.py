from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
import os


FTP_USER = "myuser"
FTP_PASSWORD = "change_this_password"


class ServerFTP:
    ADDRESS = '127.0.0.1'
    PORT = 34567

    def __init__(self) -> None:
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user(FTP_USER, FTP_PASSWORD, os.getcwd(), perm='elradfmw')

        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer

        self.server = FTPServer((ServerFTP.ADDRESS, ServerFTP.PORT), self.handler)

        self.server.max_cons = 256
        self.server.max_cons_per_ip = 5

        logging.basicConfig(filename='pyftpd.log', level=logging.INFO)

        self.server.serve_forever()


ServerFTP()

#https://pyftpdlib.readthedocs.io/en/latest/tutorial.html#id6