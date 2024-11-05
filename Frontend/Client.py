import socket
import os
import pickle
import tempfile

from Encryption import encrypt, decrypt
from messages import MessageAPI


class Client:
    def __init__(self):
        self.PORT = 5071
        self.SERVER = "146.179.86.135"
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.NO_FILES_REPLY = "None"

        self.my_files = ""

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def log_in(self, username, password):
        self.send(MessageAPI.LOG_IN_MESSAGE)
        reply = self.send(f"{username}, {password}")

        if reply == MessageAPI.LOG_IN_SUCCESSFUL_REPLY:
            data = self.client.recv(1024)
            self.my_files = pickle.loads(data)

        return reply, self.my_files


    def sign_up(self, username, password):
        self.send(MessageAPI.SIGN_UP_MESSAGE)
        self.my_files = ""

        return self.send(f"{username}, {password}")


    def download(self, file):
        self.send(MessageAPI.DOWNLOAD_MESSAGE)

        while len(file) < 4 or file[-4] != ".":
            print("Error. Invalid extension.")

        while file not in self.my_files:
            print("Error. File not found.")

            while len(file) < 4 or file[-4] != ".":
                print("Error. Invalid extension.")

        key_file = tempfile.NamedTemporaryFile(delete=False)

        self.client.send(file.encode(self.FORMAT))
        enc_data = self.client.recv(131072)
        key_data = self.client.recv(131072)

        if self.file_exists(file):
            i = 1
            while os.path.exists(f"[{i}].".join(file.split("."))):
                i += 1

            file = f"[{i}].".join(file.split("."))

        with open(file, "wb") as f:
            f.write(enc_data)

        with open(key_file.name, "wb") as f:
            f.write(key_data)

        decrypt(file, key_file.name)
        key_file.close()
        os.unlink(key_file.name)


    def upload(self, plain_file):
        self.send(MessageAPI.UPLOAD_MESSAGE)

        plain_file = plain_file.split("/")[-1]
        if plain_file in self.my_files:
            i = 1

            while f"[{i}].".join(plain_file.split(".")) in self.my_files:
                i += 1

            plain_file = f"[{i}].".join(plain_file.split("."))

        enc_file, key_file = encrypt(plain_file)

        with open(enc_file.name, "rb") as file:
            file_data = file.read()

        with open(key_file.name, "rb") as file:
            key_data = file.read()

        enc_file.close()
        key_file.close()
        os.unlink(key_file.name)

        self.send(plain_file)
        self.client.send(file_data)
        self.client.send(key_data)

        return plain_file


    def send(self, message):
        self.client.send(message.encode(self.FORMAT))
        return self.client.recv(1024).decode(self.FORMAT)


    @staticmethod
    def file_exists(address):
        return os.path.exists(address) and os.path.isfile(address) and os.stat(address).st_size > 0


if __name__ == "__main__":
    client = Client()