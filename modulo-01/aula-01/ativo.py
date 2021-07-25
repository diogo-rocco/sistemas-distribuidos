import socket

HOST = 'localhost' #IP do passivo
PORTA = 5000 # porta definida pelo passivo

#criar o descritor de socket
sock = socket.socket() #por default, ela usa AF_INET e SOCK_STREAM

#estabelecer conexao
sock.connect((HOST, PORTA))

#enviar mensagem de ola para o passivo
sock.send(b'Ola, sou o lado ativo!')

#receber mensagem do lado passivo
msg = str(sock.recv(1024), 'utf-8')
print(msg)

#encerrar conexao
print('encerrando o socket do lado ativo')
sock.close()

