import socket
import threading
import netifaces
from cryptography.fernet import Fernet

class NetworkManager:
    def __init__(self, gui):
        self.gui = gui
        self.devices = []
        self.running = True
        self.broadcast_port = 45454
        self.file_port = 45455
        self.key = Fernet.generate_key()  # For file encryption

        self.discovery_thread = threading.Thread(target=self.start_discovery)
        self.discovery_thread.start()
    
    def get_local_ip(self):
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    if addr['addr'] != '127.0.0.1':
                        return addr['addr']
        return None
    
    def start_discovery(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.broadcast_port))
            
            while self.running:
                data, addr = s.recvfrom(1024)
                if data.startswith(b"DISCOVER"):
                    device_name = data.decode().split(":")[1]
                    self.add_device(device_name, addr[0])
    
    def add_device(self, name, ip):
        if not any(d['ip'] == ip for d in self.devices):
            self.devices.append({'name': name, 'ip': ip})
            self.gui.update_device_list(self.devices)


# Add to network.py
import ssl

class NetworkManager:
    # ... previous code ...
    
    def send_file(self, file_path, dest_ip):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations('certificates/device.crt')
        
        with socket.create_connection((dest_ip, self.file_port)) as sock:
            with context.wrap_socket(sock, server_hostname=dest_ip) as ssock:
                encrypted_data = SecurityManager.encrypt_file(file_path, self.key)
                ssock.sendall(encrypted_data)
    
    def start_file_server(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('certificates/device.crt', 'certificates/device.key')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', self.file_port))
            s.listen()
            with context.wrap_socket(s, server_side=True) as ssock:
                while self.running:
                    conn, addr = ssock.accept()
                    threading.Thread(target=self.handle_connection, args=(conn,)).start()
    
    def handle_connection(self, conn):
        try:
            data = conn.recv(1024)
            # Handle file decryption and saving
        finally:
            conn.close()