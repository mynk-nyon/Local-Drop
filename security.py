from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import time

class SecurityManager:
    def __init__(self):
        self.active_sessions = {}
        
    def generate_session_key(self):
        return Fernet.generate_key()
    
    def encrypt_file(self, file_path, key):
        fernet = Fernet(key)
        with open(file_path, 'rb') as f:
            data = f.read()
        return fernet.encrypt(data)
    
    def decrypt_file(self, encrypted_data, key):
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data)
    
    def store_session(self, encrypted_data, key):
        session_id = base64.urlsafe_b64encode(os.urandom(32)).decode()
        self.active_sessions[session_id] = {
            'data': encrypted_data,
            'key': key,
            'timestamp': time.time()
        }
        return session_id
    
    def retrieve_session(self, session_id):
        session = self.active_sessions.pop(session_id, None)
        if session and time.time() - session['timestamp'] < 3600:  # 1hr expiry
            return session['data'], session['key']
        return None, None