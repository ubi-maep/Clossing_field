from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, gethostbyname, gethostname
from multiprocessing import Pipe, Process, Queue

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
        self.clqueue = Queue()
        self.p_pipe, self.c_pipe = Pipe()
        self.addrs = []
        
        self.tcpServSock = socket(AF_INET, SOCK_STREAM)
        self.tcpServSock.bind((self.ADDR, self.PORT))

    def loop_handler(self, conn, addr, dataqueue):
        while True:
            data = conn.recv(self.BUFFSIZE)
            if not data:
                break
            try:
                dataqueue.put(data.decode('utf-8'))
            except Exception as e:
                print(e)
                break
        
    def setPipe(self, conn):
        self.proc_conn = conn

    def sendData(self, dataname):
        if dataname == 'addr':
            self.proc_conn.send(self.addrs)
            return True
        elif dataname == 'data':
            if self.p_pipe.poll():
                self.proc_conn.send(self.p_pipe.recv())
                return True
            return False
        else:
            return False

    def pipeprocess(self):
        datalist = []
        while True:
            if not self.clqueue.empty():
                datalist.append(self.clqueue.get())
                self.c_pipe.send(datalist)

                

    def run(self):
        self.tcpServSock.listen(self.backlog)

        pipeproc = Process(target=self.pipeprocess, daemon=True)
        pipeproc.start()

        while True:
            try:
                conn, addr = self.tcpServSock.accept()
            except KeyboardInterrupt:
                self.tcpServSock.close()
                break

            self.addrs.append(addr)
            clproc = Process(target=self.loop_handler, args=(conn, addr, self.clqueue), daemon=True)
            clproc.start()
            self.processes.append(clproc)