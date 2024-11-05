import mariadb
import sys


class DB:
    def __init__(self):
        DB.database_check()

        try:
            self.conn = mariadb.connect(user='root',
                                        password='root',
                                        host="127.0.0.1",
                                        port=3306,
                                        database='file_storage_db')
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)


        self.cursor = self.conn.cursor()


    @staticmethod
    def database_check():
        try:
            conn = mariadb.connect(user='root',
                                   password='root',
                                   port=3306,
                                   database='file_storage_db')
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        my_cursor = conn.cursor()

        my_cursor.execute("CREATE DATABASE IF NOT EXISTS file_storage_db;")

        my_cursor.execute("CREATE TABLE IF NOT EXISTS file_storage_db.Users (\
                               UserName VARCHAR(255) PRIMARY KEY NOT NULL, \
                               UserPassword VARCHAR(255) NOT NULL);")

        my_cursor.execute("CREATE TABLE IF NOT EXISTS file_storage_db.Files (\
                              FileName VARCHAR(255) NOT NULL, \
                              UserName VARCHAR(255) NOT NULL, \
                              SymKey BLOB NOT NULL, \
                              FOREIGN KEY (UserName) REFERENCES file_storage_db.Users(UserName),\
                              PRIMARY KEY (FileName, UserName));")

        conn.close()


    def new_user(self, user, password):
        try:
            self.cursor.execute(
                f"INSERT INTO file_storage_db.Users (UserName, UserPassword) \
                  VALUES (\"{user}\", \"{password}\");")

            self.conn.commit()

        except mariadb.Error as e:
            print(f"Error when querying MariaDB: {e}")
            return False
        else:
            print("User created successfully")
            return True


    def new_file(self, user, file_name, key):
        try:
            self.cursor.execute(
                f"INSERT INTO file_storage_db.Files (FileName, UserName, SymKey) \
                  VALUES (?, ?, ?);", (file_name, user, key))
            self.conn.commit()
        except mariadb.Error as e:
            print(f"Error when querying MariaDB: {e}")
            return False
        else:
            return True


    def check_user(self, user, password):
        try:
            self.cursor.execute(
                f"SELECT COUNT(UserName) FROM file_storage_db.Users \
                  WHERE UserName = \"{user}\" AND UserPassword = \"{password}\";")

        except mariadb.Error as e:
            print(f"Error when querying MariaDB: {e}")

        return (1,) in self.cursor


    def get_key(self, user, file_name):
        try:
            self.cursor.execute(
                f"SELECT SymKey FROM file_storage_db.Files \
                  WHERE UserName = \"{user}\" AND FileName = \"{file_name}\";")
        except mariadb.Error as e:
            print(f"Error when querying MariaDB: {e}")
            return False

        for key in self.cursor:
            return key[0]
        else:
            return False


