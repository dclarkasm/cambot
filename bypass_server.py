#!/usr/bin/env python3
import socket
import time

class ShutdownBypass:
    def __init__(self):
        self.client_ip = "192.168.1.10"
        self.port = 5005
        self.message = "BYPASS"
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        # timeout for waiting for ACK from client
        self.sock.settimeout(1)
    
    def sendBypass(self):
        while True:
            print("Sending message: " + str(self.message))
            self.sock.sendto(self.message.encode(), (self.client_ip, self.port))
            try:
                data, addr = self.sock.recvfrom(1024)
                if (addr[0] == self.client_ip) and (data.decode() == "ACK"):
                    print("ACK received")
                    return
            except socket.timeout:
                print("Timed out waiting for ACK")

    def close(self):
        self.sock.close()
        print("Socket closed")

if __name__ == "__main__":
    sb = None
    try:
        sb = ShutdownBypass()
        sb.sendBypass()
    finally:
        if sb is not None:
            sb.close()
