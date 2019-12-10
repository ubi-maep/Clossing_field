from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, gethostbyname, gethostname
from multiprocessing import Pipe, Process

class UDPServer(Process):

    def __init__(self, PORT=1919):
        Process.__init__(self)
        self.data = 'hoge'
        self.kill_flag = False
        self.ADDR = '127.0.0.1'
        self.PORT = PORT
        self.BUFFSIZE = 1024

        self.udpServSock = socket(AF_INET, SOCK_DGRAM)
        self.udpServSock.bind((self.ADDR, self.PORT))

    def run(self):
        while True:
            try:
                data, self.addr = self.udpServSock.recvfrom(self.BUFFSIZE)
                self.data = data.decode()
            except:
                pass


class TCPServer(Process):

    def __init__(self, PORT=1919):
        Process.__init__(self)
        self.data = 'hoge'
        self.kill_flag = False
        self.ADDR = '127.0.0.1'
        self.PORT = PORT
        self.BUFFSIZE = 1024
        self.backlog = 10

        self.processes = []
        self.conns = []
        
        self.tcpServSock = socket(AF_INET, SOCK_STREAM)
        self.tcpServSock.bind((self.ADDR, self.PORT))

    def delProc(self, num):
        print('now deleat')
        self.conns[num].close()
        self.conns.pop(num)

    def loop_handler(self, num, conn, addr, pipeconn):
        while True:
            data = conn.recv(self.BUFFSIZE)
            if not data:
                self.delProc(num)
                break
            try:
                pipeconn.send(data)
            except Exception as e:
                print(e)
                break
        
    def setPipe(self, conn):
        self.proc_conn = conn

    def run(self):
        self.tcpServSock.listen(self.backlog)
        
        while True:
            try:
                conn, addr = self.tcpServSock.accept()
            except KeyboardInterrupt:
                self.tcpServSock.close()
                break
            parent_conn, child_conn = Pipe()

            self.conns.append(parent_conn)
            process = Process(target=self.loop_handler, args=(len(self.conns) - 1, conn, addr, child_conn), daemon=True)
            process.start()
            self.proc_conn.send(self.conns)
            self.processes.append(process)
