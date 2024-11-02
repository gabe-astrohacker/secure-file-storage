import secrets
import tempfile


def encrypt(file_in: str) -> tuple[tempfile.NamedTemporaryFile, tempfile.NamedTemporaryFile]:
    plain_data = _read_data(file_in)
    cypher_data, key = _encrypt_vernam(plain_data)

    tmp_enc = tempfile.NamedTemporaryFile(delete=False)
    tmp_key = tempfile.NamedTemporaryFile(delete=False)

    _write_data(tmp_enc.name, cypher_data)
    _write_data(tmp_key.name, key)
    return tmp_enc, tmp_key


def decrypt(file_enc: str, file_key: str) -> None:
    cypher_data = _read_data(file_enc)
    key = _read_data(file_key)

    plain_data = _decrypt_vernam(cypher_data, key)

    _write_data(file_enc, plain_data)


def _encrypt_vernam(plain_data: bytes) -> tuple[bytes, bytes]:
    plain_len = len(plain_data)
    key = secrets.randbits(plain_len * 8).to_bytes(plain_len, 'big')

    cypher_data = bytes([a ^ b for (a, b) in zip(plain_data, key)])
    return cypher_data, key


def _decrypt_vernam(cypher_data: bytes, key: bytes) -> bytes:
    return bytes([a ^ b for (a, b) in zip(cypher_data, key)])


def _read_data(file_name: str) -> bytes:
    with open(file_name, "rb") as file:
        return file.read()


def _write_data(file_name: str, data: bytes) -> None:
    with open(file_name, "wb") as file:
        file.write(data)
