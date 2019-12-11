import time
from multiprocessing import Process, Pipe
import server_class

def main():
    parent_conn, child_conn = Pipe()
    proc = server_class.TCPServer()
    proc.setPipe(child_conn)
    proc.start()

    while True:
        conns = []
        try:
            if not proc.sendData('data'):
                continue

            if parent_conn.poll():
                print(parent_conn.recv())
            
            time.sleep(1)
                
        except KeyboardInterrupt as e:
            print(e)
            break

if __name__ == '__main__':
    main()