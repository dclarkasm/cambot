#!/usr/bin/env python3
import socket
import time

class ShutdownBypass:
    def __init__(self):
        client_ip = "192.168.1.10"
        port = 5005
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    
    def sendBypass(self):
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        while True:
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            time.sleep(1)

if __name__ == "__main__":
    sb = ShutdownBypass()
    sb.sendBypass()
