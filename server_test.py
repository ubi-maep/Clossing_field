import time
from multiprocessing import Process, Pipe
import server_class

def main():
    parent_conn, child_conn = Pipe()
    proc = server_class.TCPServer()
    proc.setPipe(child_conn)
    proc.start()

    while True:
        try:
            if not proc.sendReq():
                continue

            if parent_conn.poll():
                for addr, data in parent_conn.recv():
                    print(data)
                    proc.sendADDR(addr, 'done')
                
        except KeyboardInterrupt as e:
            print(e)
            break

if __name__ == '__main__':
    main()