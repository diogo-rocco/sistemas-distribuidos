import socket
import select
import sys
import multiprocessing

#define a localizacao do servidor
HOST = ''
PORTA = 5000

input_list = [sys.stdin]
client_list = []

def startServer():
    sock = socket.socket() #default AF_INET e SOCK_STREAM
    sock.bind((HOST, PORTA))
    sock.listen(5)
    sock.setblocking(False)
    input_list.append(sock)
    return sock

def acceptConection(sock):
    client_sock, address = sock.accept()
    return client_sock, address

def endConection(client_sock, address):
    print('encerrando conexao com', address)
    client_sock.close()

def answerRequest(client_sock, address):
    while True:
        try:
            msg = client_sock.recv(1024)
            if not msg:
                endConection(client_sock, address)
                return
            
            print(str(address) + ': ' + str(msg, 'utf-8'))
            client_sock.send(msg)
        except:
            endConection(client_sock, address)
            return

def server():
    sock = startServer()
    print('pronto para receber conexoes...')
    while True:
        #print(input_list)
        read, write, excep = select.select(input_list, [], [])
        for ready in read:
            if ready == sock:
                client_sock, address = acceptConection(sock)
                print('estabelecendo conexao com', address)
                client = multiprocessing.Process(target=answerRequest, args=(client_sock, address))
                client_list.append(client)
                client.start()
            
            elif ready == sys.stdin:
                comand = input()
                if comand == 'fim':
                    for c in client_list:
                        c.join()
                    sock.close
                    return

server()
