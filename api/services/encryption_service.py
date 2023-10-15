import base64
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


class EncryptionServices:
    def encrypt(self, password):
        load_dotenv()
        key = base64.b64encode(
            f"{os.environ.get('ENCRYPTION_PASSWORD'):<32}".encode("utf-8")
        )
        encryptor = Fernet(key=key)
        encrypted_password = encryptor.encrypt(password.encode("utf-8"))
        return encrypted_password

    def decrypt(self, encrypted_password):
        load_dotenv()
        key = base64.b64encode(
            f"{os.environ.get('ENCRYPTION_PASSWORD')}".encode("utf-8")
        )
        encryptor = Fernet(key=key)
        decrypted_password = encryptor.decrypt(encrypted_password).decode("utf-8")
        return decrypted_password
