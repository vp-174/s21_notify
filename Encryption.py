from Imports import *
class Encryption:
    def __init__(self, key="s21"):
        self.key = key

    def encrypt(self, password):
        return base64.b64encode((password + self.key).encode()).decode()

    def decrypt(self, encrypted_password):
        decrypted_password = base64.b64decode(encrypted_password.encode()).decode()
        return decrypted_password.replace(self.key, '')