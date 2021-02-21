#!/usr/bin/env python3
import socket

class ShutdownBypassClient:
    def __init__(self):
        self.server_ip = "0.0.0.0"  # 0.0.0.0 to bind to any IP
        self.port = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.server_ip, self.port))
        # server should send messages faster than this timeout to prevent race condition
        self.sock.settimeout(5)  
    
    def isBypass(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            print("Received message: " + str(message))
            if message == "BYPASS":
                self.sock.sendto("ACK".encode(), addr)
                return True
        except socket.timeout:
            print("Timed out waiting for message")
        return False

    def close(self):
        self.sock.close()
        print("Socket closed")

if __name__ == "__main__":
    sb = None
    try:
        sb = ShutdownBypassClient()
        if sb.isBypass():
            exit(1)  # Don't shutdown
        exit(0)  # Shutdown
    finally:
        if sb is not None:
            sb.close()
