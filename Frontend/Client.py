import socket
import os
import pickle
import tempfile

from Encryption import encrypt, decrypt


class Client:
    def __init__(self):
        self.PORT = 5071
        self.SERVER = "192.168.1.151"
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.LOG_IN_MESSAGE = "!LOG IN"
        self.LOG_IN_SUCCESSFUL_REPLY = "Authentication successful."
        self.SIGN_UP_MESSAGE = "!SIGN UP"
        self.DOWNLOAD_MESSAGE = "!DOWNLOAD"
        self.UPLOAD_MESSAGE = "!UPLOAD"
        self.NO_FILES_REPLY = "None"

        self.username = ""
        self.password = ""
        self.reply = ""
        self.my_files = ""

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def log_in(self, username, password):
        self.send(self.LOG_IN_MESSAGE)
        self.details(username, password)

        self.send(f"{self.username}, {self.password}")

        if self.reply == self.LOG_IN_SUCCESSFUL_REPLY:
            data = self.client.recv(1024)
            self.my_files = pickle.loads(data)

        return self.reply, self.my_files


    def sign_up(self, username, password):
        self.send(self.SIGN_UP_MESSAGE)
        self.my_files = ""
        self.details(username, password)

        self.send(f"{self.username}, {self.password}")

        return self.reply


    def download(self, enc_file):
        self.send(self.DOWNLOAD_MESSAGE)

        while len(enc_file) < 4 or enc_file[-4] != ".":
            print("Error. Invalid extension.")

        while enc_file not in self.my_files:
            print("Error. File not found.")

            while len(enc_file) < 4 or enc_file[-4] != ".":
                print("Error. Invalid extension.")

        key_file = tempfile.NamedTemporaryFile(delete=False)

        self.client.send(enc_file.encode(self.FORMAT))
        enc_data = self.client.recv(131072)
        key_data = self.client.recv(131072)

        plain_file = enc_file

        if os.path.exists(plain_file):
            i = 1
            while os.path.exists(plain_file[:-4] + f"[{i}]" + plain_file[-4:]):
                i += 1

            plain_file = plain_file[:-4] + f"[{i}]" + plain_file[-4:]

        with open(plain_file, "wb") as file:
            file.write(enc_data)

        with open(key_file.name, "wb") as file:
            file.write(key_data)

        decrypt(plain_file, key_file.name)
        key_file.close()
        os.unlink(key_file.name)


    def upload(self, plain_file):
        self.send(self.UPLOAD_MESSAGE)
        i = 0

        if plain_file.split("/")[-1] in self.my_files:
            i = 1

            while plain_file.split("/")[-1][:-4] + f"[{i}]" + plain_file.split("/")[-1][:-4] in self.my_files:
                i += 1

            file_addr = plain_file.split("/")[-1][:-4] + f"[{i}]" + plain_file.split("/")[-1][-4:]

        else:
            file_addr = plain_file.split("/")[-1]

        enc_file, key_file = encrypt(plain_file)

        with open(enc_file.name, "rb") as file:
            file_data = file.read()

        with open(key_file.name, "rb") as file:
            key_data = file.read()

        enc_file.close()
        key_file.close()
        os.unlink(key_file.name)

        self.send(file_addr)
        self.client.send(file_data)
        self.client.send(key_data)

        self.reply = self.client.recv(1024).decode(self.FORMAT)
        print(self.reply + "\n\n")

        return file_addr


    def details(self, username, password):
        self.username, self.password = username, password


    def send(self, message):
        self.client.send(message.encode(self.FORMAT))
        self.reply = self.client.recv(1024).decode(self.FORMAT)
        print(self.reply + "\n\n")


    @staticmethod
    def file_check(address):
        return os.path.exists(address) and os.path.isfile(address) and os.stat(address).st_size > 0


if __name__ == "__main__":
    client = Client()