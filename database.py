import sqlite3
from typing import Any


# ---------------------------------------------------------
#   * host -> utente che sta eseguendo le operazioni
# ---------------------------------------------------------


class Database:
    PATH = 'database.db'

    def __init__(self) -> None:
        try:
            db = sqlite3.connect(Database.PATH)
            db.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT NOT NULL,
                    group_rank INTEGER NOT NULL,
                    group_founder INTEGER NOT NULL,
                    FOREING KEY(group_founder) REFERNCES users(user_id)
                );"""
            )
            db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    user_email TEXT NOT NULL,
                    user_password TEXT NOT NULL,
                    user_rank INTEGER NOT NULL
                );"""
            )
            db.execute("""
                CREATE TABLE IF NOT EXISTS membership_group (
                    user_id INTEGER PRIMARY KEY,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    group_id INTEGER,
                    FOREIGN KEY(group_id) REFERENCES groups(group_id)
                )"""
            )
        except Exception as e:
            print(repr(e))
    
    def createUser(self, host:str, user_name:str, user_email:str, user_password:str) -> None: #user_rank default 0
        pass

    def createGroup(self, host:str, gropu_name:str, group_fonder:int) -> None: #group_rank default 0
        pass

    def getData(self, host:str, query:str) -> Any:
        pass

    def setData(self, host:str, query:str) -> Any:
        pass
