import socket
import threading
from ifaddr import get_adapters
from flask import current_app

class NetworkManager:
    def __init__(self):
        self.discovery_port = 5353
        self.broadcast_ip = self.get_broadcast_address()
        self.running = True
        

def get_broadcast_address(self):
    for adapter in get_adapters():
        for ip in adapter.ips:
            if ip.is_IPv4 and ip.network_prefix < 32:
                    try:
                        return str(ip.network.broadcast_address)
                    except AttributeError:
                        continue
        return '255.255.255.255'
    
    def discover_devices(self):
        # Send discovery packet
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(b'DISCOVER', (self.broadcast_ip, self.discovery_port))
        
        # Listen for responses
        devices = []
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.bind(('', self.discovery_port))
            
            try:
                while True:
                    data, addr = s.recvfrom(1024)
                    if data.startswith(b'RESPONSE'):
                        device_info = data.decode().split('|')[1]
                        devices.append({
                            'ip': addr[0],
                            'info': device_info
                        })
            except socket.timeout:
                pass
        
        return devices