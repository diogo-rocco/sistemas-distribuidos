import socket
import select
import sys

#define a localizacao do servidor
HOST = ''
PORTA = 5000

input_list = [sys.stdin]

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

def answerRequest(client_sock, address):
    while True:
        try:
            msg = client_sock.recv(1024)
            if not msg:
                print('encerrando conexao com', address)
                client_sock.close()
                break
            print(str(address) + ': ' + str(msg, 'utf-8'))
            client_sock.send(msg)
        except:
            print('encerrando conexao com', address)
            client_sock.close()
            break

def server():
    sock = startServer()
    print('pronto para receber conexoes...')
    while True:
        read, write, excep = select.select(input_list, [], [])
        for ready in read:
            if ready == sock:
                client_sock, address = acceptConection(sock)
                print('estabelecendo conexao com', address)
                answerRequest(client_sock, address)
            
            elif ready == sys.stdin:
                comand = input()
                if comand == 'fim':
                    sock.close
                    return

server()
