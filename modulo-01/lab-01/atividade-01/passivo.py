import socket

HOST = ''
PORTA = 5000

sock = socket.socket() #default AF_INET e SOCK_STREAM

sock.bind((HOST, PORTA))
sock.listen(1)

new_sock, address = sock.accept()

while True:
    msg = new_sock.recv(1024)
    if not msg:
        break
    print(str(msg, 'utf-8'))

print('encerrando conexao do lado passivo')
sock.close()