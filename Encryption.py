import base64
import hashlib
from cryptography.fernet import Fernet


class Encryption:
    _KEY = base64.urlsafe_b64encode(hashlib.sha256(b's21').digest())

    def __init__(self):
        self.cipher = Fernet(self._KEY)

    def encrypt(self, password):
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password):
        return self.cipher.decrypt(encrypted_password.encode()).decode()