from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

class UDPClnt():

    def __init__(self):
        self.ADDR = '127.0.0.1'
        self.PORT = 1919
        self.BUFSIZE = 1024

        self.udpClntSock = socket(AF_INET, SOCK_DGRAM)
       
    def send(self, data):
        self.udpClntSock.sendto(data.encode('utf-8'), (self.ADDR, self.PORT))

    def close(self):
        self.udpClntSock.close()

class TCPClnt():

    def __init__(self):
        self.ADDR = '127.0.0.1'
        self.PORT = 1919
        self.BUFSIZE = 1024

        self.tcpClntSock = socket(AF_INET, SOCK_STREAM)
        self.tcpClntSock.connect((self.ADDR, self.PORT))

    def send(self, data):
        self.tcpClntSock.send(data.encode('utf-8'))

    def catch(self):
        return self.tcpClntSock.recv(self.BUFSIZE).decode('utf-8')

    def close(self):
        self.tcpClntSock.close()        