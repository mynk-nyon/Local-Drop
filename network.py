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