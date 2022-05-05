from ftplib import FTP

with FTP(source_address=('127.0.0.1', 34567), user='myuser', passwd='change_this_password') as ftp:
    ftp.login()