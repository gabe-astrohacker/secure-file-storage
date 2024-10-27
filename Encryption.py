import secrets


class Encryption:
    def __init__(self, file_in, file_out):
        if type(file_in) == tuple:
            self.file_in, self.key_file = file_in[0]
        elif type(file_in) == str:
            self.file_in = file_in

        self.file_out = file_out

        self.plain_data = b""
        self.cypher_data = b""
        self.key = b""


    def encrypt(self):
        self.plain_data = Encryption.read_data(self.file_in)

        self.encrypt_vernam()

        Encryption.write_data(self.file_out, self.cypher_data)
        Encryption.write_data(self.file_out[:-4] + "_key" + self.file_out[-4:], self.key)

    def decrypt(self):
        self.cypher_data = Encryption.read_data(self.file_in)
        self.key = Encryption.read_data(self.key_file)

        self.decrypt_vernam()

        Encryption.write_data(self.file_out, self.plain_data)


    @staticmethod
    def read_data(file_in):
        with open(file_in, "rb") as file:
            return file.read()

    @staticmethod
    def write_data(file_address, data):
        with open(file_address, "wb") as file:
            file.write(data)


    def encrypt_vernam(self):
        plain_len = len(self.plain_data)
        self.key = secrets.randbits(plain_len * 8).to_bytes(plain_len, 'big')

        self.cypher_data = bytes([a ^ b for (a, b) in zip(self.plain_data, self.key)])


    def decrypt_vernam(self):
        self.plain_data = bytes([a ^ b for (a, b) in zip(self.cypher_data, self.key)])




