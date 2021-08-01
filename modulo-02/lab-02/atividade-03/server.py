import socket
from pickle import loads
import pathlib

#função responsavel pela contagem das palavras no arquivo
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

HOST = ''
PORTA = 5000

#inicialização do socket
sock = socket.socket()
sock.bind((HOST, PORTA))
sock.listen(1)

#faz nosso servidor entrar em loop infinito 
while True:
    #estabelecimento da conexão
    new_sock, address = sock.accept()

    while True:
        msg = new_sock.recv(1024) #recebe a mensagem
        if not msg: #sai do loop quando o cliente para de enviar mensagens
            break
        msg = loads(msg) #passa a mensagem de uma sequencia de bytes para um objeto (dicionario)
        new_sock.send(str(word_counter(msg['file_name'], msg['word'])).encode('utf-8')) #chama a função de contagem de palavras e envia a resposta no formato de série de bytes

    new_sock.close() #encerra o socket