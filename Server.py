import socket
import threading

from Database import DB
import os


class Server:
    def __init__(self):
        self.PORT = 5050
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        self.auth = False

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        print("[STARTING] server is starting...")

        self.server.listen()
        print(f"[LISTENING] server is listening on {self.SERVER_IP}")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


    class User:
        def __init__(self, conn, addr):
            self.conn = conn
            self.addr = addr
            self.username = ""
            self.password = ""


    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} is requesting to connect.\n")

        user = self.User(conn, addr)
        client_request = self.receive(user)

        while client_request != self.DISCONNECT_MESSAGE:
            if client_request == "!LOG IN":
                self.authentication(user)
                if self.auth:
                    user_files = ""
                    for a_file in os.listdir(f"server_folder/{user.username}"):
                        user_files += a_file + " "

                    if user_files == "":
                        user_files = "None"
                    elif user_files[-1] == " ":
                        user_files = user_files[:-1]

                    user.conn.send(user_files.encode(self.FORMAT))

            elif client_request == "!SIGN UP":

                self.create_account(user)

            elif self.auth:
                if client_request == "!UPLOAD":
                    self.upload(user)

                elif client_request == "!DOWNLOAD":
                    self.download(user)

                else:
                    user.conn.send("Error. Invalid request.".encode(self.FORMAT))

            client_request = self.receive(user)

        user.conn.send("Goodbye.".encode(self.FORMAT))
        user.conn.close()


    def receive(self, user, msg="Message Received."):
        request = user.conn.recv(2048).decode(self.FORMAT)
        print(f"[{user.addr}] {request}")
        user.conn.send(msg.encode(self.FORMAT))
        return request


    def authentication(self, user):
        user.username, user.password = self.receive(user, msg="").split(", ")

        db = DB()
        self.auth = db.check_user(user.username, user.password)

        if self.auth:
            user.conn.send("Authentication successful.".encode(self.FORMAT))
        else:
            user.conn.send("Invalid username or password.".encode(self.FORMAT))


    def create_account(self, user):
        user.username, user.password = self.receive(user, msg="").split(", ")

        db = DB()
        sign_up = db.new_user(user.username, user.password)

        if sign_up:
            user.conn.send("User created successfully".encode(self.FORMAT))
            os.makedirs(f"server_folder/{user.username}")
        else:
            user.conn.send("Username already in use. Try again.".encode(self.FORMAT))


    def upload(self, user):
        file_name = self.receive(user)
        file_data = user.conn.recv(131072)
        key_data = user.conn.recv(131072)

        user.conn.send("Msg received".encode(self.FORMAT))

        db = DB()
        db.new_file(user.username, file_name, key_data)

        with open(f"server_folder/{user.username}/{file_name}", "wb") as file:
            file.write(file_data)


    def download(self, user):
        file_name = self.receive(user, msg="")

        with open(f"server_folder/{user.username}/{file_name}", "rb") as file:
            data = file.read()

        db = DB()
        key = db.get_key(user.username, file_name)
        user.conn.send(data)
        user.conn.send(key)


if __name__ == "__main__":
    server = Server()
