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

        self.clqueue = Queue()
        self.recv_dpipe, self.send_dpipe = Pipe()
        self.recv_spipe, self.send_spipe = Pipe()
        self.recv_s2, self.send_s2 = Pipe()
        
        self.tcpServSock = socket(AF_INET, SOCK_STREAM)
        self.tcpServSock.bind((self.ADDR, self.PORT))
        
    def setPipe(self, conn):
        self.proc_conn = conn

    def sendReq(self):
        if self.recv_dpipe.poll():
            self.proc_conn.send(self.recv_dpipe.recv())
            return True
        else:
            return False

    def sendADDR(self, addr, data):
        self.send_s2.send([addr, data])

    def sendALL(self, data):
        print('b')
        
    def recv_handler(self, conn, addr, dataqueue):
        while True:
            data = conn.recv(self.BUFFSIZE)
            if not data:
                break
            try:
                datataple = (addr, data.decode('utf-8'))
                dataqueue.put(datataple)
            except Exception as e:
                print(e)
                break

    def send_handler(self, conn, addr, pipe):
        while True:
            if pipe.poll():
                conn.send(pipe.recv().encode('utf-8'))

    def data_manager(self):

        datalist = []
        pipedict = {}
        while True:
            if not self.clqueue.empty():
                datalist.append(self.clqueue.get())
                self.send_dpipe.send(datalist)
                datalist.clear()
        
            if self.recv_spipe.poll():
                pipedict = self.recv_spipe.recv()
            
            if self.recv_s2.poll():
                plist = self.recv_s2.recv()
                pipedict[plist[0]].send(plist[1])
                

    def run(self):
        self.tcpServSock.listen(self.backlog)
        pipedict = {}

        manageproc = Process(target=self.data_manager, daemon=True)
        manageproc.start()

        while True:

            try:
                conn, addr = self.tcpServSock.accept()
            except KeyboardInterrupt:
                self.tcpServSock.close()
                break
            
            part_send, part_recv = Pipe()
            pipedict[addr] = part_send
            self.send_spipe.send(pipedict)

            recvproc = Process(target=self.recv_handler, args=(conn, addr, self.clqueue), daemon=True)
            sendproc = Process(target=self.send_handler, args=(conn, addr, part_recv), daemon=True)
            recvproc.start()
            sendproc.start()