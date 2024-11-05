import socket
import threading
import pickle
import os

from Backend.Database import DB
from messages import MessageAPI


class Server:
    def __init__(self):
        self.PORT = 5050
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.db = DB()

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
            self.auth = False
            self.username = ""
            self.password = ""

    def handle_client(self, conn: socket, addr) -> None:
        print(f"[NEW CONNECTION] {addr} is requesting to connect.\n")

        user = self.User(conn, addr)
        client_request = self.receive(user)

        while client_request != MessageAPI.DISCONNECT_MESSAGE:
            match client_request:
                case MessageAPI.SIGN_UP_MESSAGE:
                    self.create_account(user)

                case MessageAPI.LOG_IN_MESSAGE:
                    if self.authentication(user):
                        user_files = os.listdir(f"server_folder/{user.username}")
                        user.conn.send(pickle.dumps(user_files))

                case MessageAPI.UPLOAD_MESSAGE | MessageAPI.DOWNLOAD_MESSAGE:
                    if not user.auth:
                        user.conn.send("Error. User not authenticated.".encode(self.FORMAT))
                        user.conn.close()

                    if client_request == MessageAPI.UPLOAD_MESSAGE:
                        self.upload(user)
                    else:
                        self.download(user)
                case _:
                    user.conn.send("Error. Invalid request.".encode(self.FORMAT))

            client_request = self.receive(user)

        user.conn.send("Goodbye.".encode(self.FORMAT))
        user.conn.close()

    def receive(self, user: User, msg="Message Received.") -> str:
        request = user.conn.recv(2048).decode(self.FORMAT)
        print(f"[{user.addr}] {request}")
        user.conn.send(msg.encode(self.FORMAT))
        return request

    def authentication(self, user: User) -> None:
        user.username, user.password = self.receive(user, msg="").split(", ")

        auth = self.db.check_user(user.username, user.password)
        user.auth = auth

        reply = MessageAPI.LOG_IN_SUCCESSFUL_REPLY if auth else MessageAPI.LOG_IN_FAILED_REPLY
        user.conn.send(reply.encode(self.FORMAT))
        return auth

    def create_account(self, user: User) -> None:
        user.username, user.password = self.receive(user, msg="").split(", ")

        sign_up = self.db.new_user(user.username, user.password)

        if sign_up:
            user.conn.send("User created successfully".encode(self.FORMAT))
            os.makedirs(f"server_folder/{user.username}")
        else:
            user.conn.send("Username already in use. Try again.".encode(self.FORMAT))

    def upload(self, user: User) -> None:
        file_name = self.receive(user)
        file_data = user.conn.recv(131072)
        key_data = user.conn.recv(131072)

        self.db.new_file(user.username, file_name, key_data)

        with open(f"server_folder/{user.username}/{file_name}", "wb") as file:
            file.write(file_data)

    def download(self, user: User) -> None:
        file_name = self.receive(user, msg="")

        with open(f"server_folder/{user.username}/{file_name}", "rb") as file:
            data = file.read()

        key = self.db.get_key(user.username, file_name)
        user.conn.send(data)
        user.conn.send(key)


if __name__ == "__main__":
    server = Server()
