import client_class

def main():
    clnt = client_class.TCPClnt()

    while True:
        try:
            data = input('%s > ' % 'Client')
            clnt.send(data)
            print(clnt.catch())
            if not data:
                clnt.close()
                break
        except KeyboardInterrupt as e:
            print(e)
            clnt.close()
            break

if __name__ == '__main__':
    main()