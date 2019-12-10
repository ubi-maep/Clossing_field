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
            if parent_conn.poll():
                for conn in parent_conn.recv():
                    conns.append(conn)
                while True:
                    if parent_conn.poll():
                        print('reload')
                        break
                    for conn in conns:
                        if conn.poll():
                            print(conn.recv().decode('utf-8'))
        except KeyboardInterrupt as e:
            print(e)
            break

if __name__ == '__main__':
    main()