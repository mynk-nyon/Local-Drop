from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

class SecurityManager:
    @staticmethod
    def encrypt_file(file_path, key):
        fernet = Fernet(key)
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        return encrypted
    
    @staticmethod
    def decrypt_file(encrypted_data, key):
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data)
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None):
        if not salt:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))