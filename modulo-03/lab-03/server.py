import socket
import select
import sys
import threading
import pathlib
from pickle import loads

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

def word_counter(file_name, word):
    try:
        ocurrences = 0
        path = str(pathlib.Path(__file__).parent.resolve())+'/resources/' #caminho até o diretório com os arquivos
        
        with open(path+file_name, encoding='utf-8') as file: #abre o arquivo
            for line in file: #itera sobre todas as linhas do arquivo
                line = line.replace('.', '').replace(',', '').replace(':', '').replace('(', '').replace(')', '') #remoção de caracteres especiais
                for current_word in line.split(): #separa a linha em um array de palavras e itera sobre esse array
                    if current_word.lower() == word: ocurrences += 1 #caso encontre a palavra, soma 1 no contador de palavras
        return ocurrences
    
    except: #caso haja alguma excessão (o arquivo não exista) retorna o código de erro
        return -1

def answerRequest(client_sock, address):
    while True:
        try:
            msg = client_sock.recv(1024)
            if not msg:
                endConection(client_sock, address)
                return
            
            msg = loads(msg)
            client_sock.send(str(word_counter(msg['file_name'], msg['word'])).encode('utf-8'))
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
                client = threading.Thread(target=answerRequest, args=(client_sock, address))
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
