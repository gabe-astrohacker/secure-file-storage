import socket
import os

from Encryption import Encryption


class Client:
    def __init__(self):
        self.PORT = 5050
        self.SERVER = "192.168.1.151"
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.username = ""
        self.password = ""
        self.reply = ""
        self.my_files = ""

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def log_in(self, username, password):
        self.send("!LOG IN")
        self.details(username, password)

        self.send(f"{self.username}, {self.password}")

        if self.reply == "Authentication successful.":
            self.my_files = self.client.recv(1024).decode(self.FORMAT).split()

            if self.my_files[0] == "None":
                self.my_files = ["No files have been uploaded yet."]

        return self.reply, self.my_files


    def sign_up(self, username, password):
        self.send("!SIGN UP")
        self.my_files = ""
        self.details(username, password)

        self.send(f"{self.username}, {self.password}")

        return self.reply


    def download(self, enc_file):
        self.send("!DOWNLOAD")

        while len(enc_file) < 4 or enc_file[-4] != ".":
            print("Error. Invalid extension.")

        while enc_file not in self.my_files:
            print("Error. File not found.")

            while len(enc_file) < 4 or enc_file[-4] != ".":
                print("Error. Invalid extension.")

        key_file = enc_file[:-4] + "_key" + enc_file[-4:]

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

        with open(key_file, "wb") as file:
            file.write(key_data)

        download_file = Encryption((plain_file, key_file), plain_file)
        download_file.decrypt()

        os.remove(key_file)


    def upload(self, plain_file):
        self.send("!UPLOAD")
        i = 0

        if plain_file.split("/")[-1] in self.my_files:
            i = 1

            while plain_file.split("/")[-1][:-4] + f"[{i}]" + plain_file.split("/")[-1][:-4] in self.my_files:
                i += 1

            file_addr = plain_file.split("/")[-1][:-4] + f"[{i}]" + plain_file.split("/")[-1][-4:]

        else:
            file_addr = plain_file.split("/")[-1]

        if i == 0:
            to_enc_addr = plain_file[:-4] + "_enc" + plain_file[-4:]
        else:
            to_enc_addr = file_addr

        upload_file = Encryption(plain_file, to_enc_addr)
        upload_file.encrypt()

        key_addr = to_enc_addr[:-4] + "_key" + to_enc_addr[-4:]

        with open(to_enc_addr, "rb") as file:
            file_data = file.read()

        with open(key_addr, "rb") as file:
            key_data = file.read()

        self.send(file_addr)
        self.client.send(file_data)
        self.client.send(key_data)

        self.reply = self.client.recv(1024).decode(self.FORMAT)
        print(self.reply + "\n\n")

        os.remove(to_enc_addr)
        os.remove(key_addr)

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