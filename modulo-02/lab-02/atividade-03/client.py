import socket
from pickle import dumps

#formata a mensagem que será enviada para o usuário com base no código enviado para o servidor
def format_message(response_code):
    if response_code<0:
        return 'Arquivo não encontrado, verifique se o arquivo está correto e tente novamente'
    else:
        return 'Foram encontradas ' + str(response_code) + ' ocorrências da palavra no arquivo'

HOST = 'localhost'
PORTA = 5000

#inicia o socket
sock = socket.socket()

#estabelece a conexão
sock.connect((HOST,PORTA))

while True:
    file_name = input('Digite o nome do arquivo onde deseja fazer a busca: ') #recebe o nome do arquivo
    if file_name[-4:] != '.txt': file_name = file_name+'.txt' #caso o nome tenha sido fornecido sem a extensão .txt, adiciona a extensão no nome do arquivo
    
    word = input('Digite o nome da palavra que deseja buscar: ') # recebe a palavra de busca

    msg = {'file_name': file_name, 'word': word} #gera o objeto que será enviado para o servidor
    msg_encoded = dumps(msg) #converte o objeto em uma sequencia de bytes

    sock.send(msg_encoded) #envia a mensagem

    response = int(sock.recv(1024)) #recebe a resposta do servidor

    print(format_message(response)) #exibe para o usuário a resposta formatada

    #confere se o usuário deseja realizar uma nova busca
    while True:
        new_search = input('deseja fazer uma nova busca? (s/n): ')
        if new_search == 's' or new_search == 'n': break
    
    if new_search == 'n': break
    print('\n')

sock.close() #encerra o socket