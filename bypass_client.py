#!/usr/bin/env python3
import socket

class ShutdownBypass:
    def __init__(self):
        server_ip = "0.0.0.0"  # Bind to any IP
        server_port = 5005
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        sock.bind((server_ip, server_port))
        sock.settimeout(3)
    
    def isBypass(self):
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if data == "BYPASS":
            return True
        return False

if __name__ == "__main__":
    sb = ShutdownBypass()
    if sb.isBypass() exit(1)  # Don't shutdown
    exit(0)  # Shutdown
