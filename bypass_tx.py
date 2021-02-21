#!/usr/bin/env python3
import socket
import time

class ShutdownBypassServer:
    def __init__(self):
        self.client_ip = "bigbird.local"
        self.port = 5005
        self.message = "BYPASS"
        self.sock = None

    def initSocket(self):
        if self.sock is not None:
            # first close and delete the socket because this function gets called many times in a row
            self.close()
            del self.sock
            self.sock = None
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        # timeout for waiting for ACK from client
        self.sock.settimeout(1)

    def sendBypass(self):
        while True:
            print("Sending message: " + str(self.message))
            try:
                self.initSocket()
                self.sock.sendto(self.message.encode(), (self.client_ip, self.port))
                data, addr = self.sock.recvfrom(1024)
                if data.decode() == "ACK":
                    print("ACK received")
                    print("BigBird Birdhouse is at address " + str(addr[0]))
                    return
            except (socket.timeout, socket.error):
                print("Timed out waiting for ACK")
                time.sleep(1)

    def close(self):
        self.sock.close()
        print("Socket closed")

if __name__ == "__main__":
    sb = None
    try:
        sb = ShutdownBypassServer()
        sb.sendBypass()
    finally:
        if sb is not None:
            sb.close()
