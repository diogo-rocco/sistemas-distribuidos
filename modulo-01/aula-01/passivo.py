import socket

HOST = '' #interface padrao de comunicao da maquina
PORTA = 5000 #identifica o processo na maquina

#criar o descritor de socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Pilha de protocolo -> internet e servico -> TCP (servico de camada de transporte com cocexao)

#vincular o endereco e porta
sock.bind((HOST, PORTA))

#colocar-se em modo de espera
sock.listen(1) #argumento indica quantidade de conexoes pendentes

#aceitar conexao
novo_sock, endereco = sock.accept() #accept eh uma funcao bloqueante, que espera ate surgir uma conexao
print('Cocentado com:', str(endereco))

while True:
    #esperar por mensagem do lado ativo
    msg = novo_sock.recv(1024) #argumento indica quantidade maxima de bytes
    if not msg:
        break
    print(str(msg, encoding='utf-8'))
    novo_sock.send(b'Ola, sou o lado passivo!')

#fechar o descritor de socket principal
print('encerrando o socket do lado passivo')
sock.close()

