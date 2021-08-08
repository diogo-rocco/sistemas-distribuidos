import socket
print('digite a mensagem que quer enviar ao lado passivo. Digite "end" para encerrar a conexao')
HOST = 'localhost'
PORTA = 5000

sock = socket.socket()

sock.connect((HOST,PORTA))

while True:
    msg = input()
    if msg == 'end':
        break
    sock.send(msg.encode('utf-8'))

print('encerrando a conexao do lado ativo')
sock.close()