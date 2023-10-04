import functools
from typing import Any, Optional, Sequence

from mysql import connector as conn

import config


# Decorator for opening and closing a connection to a database
def open_and_close_connect_to_db(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.open_connection_to_db()
        result = method(self, *args, **kwargs)
        self.close_connection_to_db()
        return result
    return wrapper


class ConnectorToDB:
    def __init__(self) -> None:
        self.connection: Any

    def open_connection_to_db(self) -> None:
        try:
            print('[INFO] Connecting to a MySQL database')
            self.connection = conn.connect(
                host = config.DB_HOST,
                port = config.DB_PORT,
                user = config.DB_USER_NAME,
                password = config.DB_USER_PASSWORD,
                database = config.DB_NAME
            )
            self.set_autocommit(True)
        except conn.Error as error:
            print("[ERROR] MySQL connection error", error)
        else:
            print("[INFO] MySQL connection opened")         
    
    def set_autocommit(self, autocommit: bool) -> None:
        self.connection.autocommit = autocommit
    
    def close_connection_to_db(self) -> None:
        if self.connection:
            self.connection.close()
            print("[INFO] MySQL connection closed")

    @open_and_close_connect_to_db
    def get_info_of_departments(self) -> Optional[Sequence[Any]]:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM jos_staffled_dep;")
                result = cursor.fetchall()
            except Exception as error:
                print("[ERROR]", error)
                return None
            else:
                print("[SUCCESS] Operation was successfully completed!")
                return result

    @open_and_close_connect_to_db
    def get_logins_of_users(self) -> Optional[list[str]]:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("SELECT login FROM jos_staffled;")
                result = cursor.fetchall()
            except Exception as error:
                print("[ERROR]", error)
                return None
            else:
                print("[SUCCESS] Operation was successfully completed!")
                return [login[0] for login in result]
    
    
if __name__ == '__main__':
    connector = ConnectorToDB()
    
    departments = connector.get_info_of_departments()
    if departments:
        print('Result:')
        for dep in departments:
            print(f'\t{dep}')
    
    logins = connector.get_logins_of_users()
    if logins:
        print('Result:')
        print(f'\t{logins}')
