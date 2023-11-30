"""Arquivo de funções que são utilizadas no programa principal"""
import os
import csv
import bcrypt #Pacote que faz o hash das senhas de usuário salvas
import ssl #Pacote que adiciona camada de segurança para comunicações em rede
import smtplib #Pacote para envio de e-mails
from email.message import EmailMessage
#from getpass import getpass #I tried using getpass, but it didn't work - the popup didn't show in the top of the screen
import requests
from pandas import read_csv
from keys import conta_email, gmail_app_pwd
from models import random_api_url, random_api_request_body
from gerenciador_senhas_classes import Login



def verificaRegistroSenhas():
    """Função que verifica se já há um arquivo csv salvo para armazenar senhas"""
    if os.path.isfile('senhas.csv'):
        return True
    else:
        return False
    

def criaArquivoSenhas():
    """Função que inicializa um arquivo de senhas com o nome 'senhas.csv'"""
    with open('senhas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["dono_senha", "dominio", "usuario", "senha"])


def verificaRegistroUsuarios():
    """Função que verifica se já há um arquivo csv salvo para armazenar usuários"""
    if os.path.isfile('usuarios.csv'):
        return True
    else:
        return False


def criaArquivoUsuarios():
    """Função que inicializa um arquivo de usuários com o nome 'usuarios.csv'"""
    with open('usuarios.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["usuario", "hash_pwd"])


def verificaRegistroRecuperacaoUsuarios():
    """Função que verifica se já há um arquivo csv salvo para armazenar logs de recuperação de senhas de usuário"""
    if os.path.isfile('log_recuperacao_senha.csv'):
        return True
    else:
        return False


def criaArquivoLogRecuperacaoUsuarios():
    """Função que inicializa um arquivo de log de recuperação de senhas de usuário com o nome 'log_recuperacao_senha.csv'"""
    with open('log_recuperacao_senha.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["usuario", "time_stamp_solicitacao", "time_stamp_limite", "codigo"])


def integridade_usuario(username: str):
    """Verifica se existe um usuário cadastrado com o username passado
    Retorna verdadeiro se o usuário não estiver cadastrado
    Retorna false se o usuário já estiver cadastrado"""
    users_table = read_csv('usuarios.csv')
    users = users_table['usuario'].tolist()

    return not(username in users)


def novoUsuario(username: str, pwd: str):
    """Função que cria/registra um novo usuário na tabela de usuários"""
    lst_usuario = [username, pwd]

    with open('usuarios.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lst_usuario)

def obtem_senha_usuario(username: str):
    """Função que recebe um username e retorna a senha correspondente"""
    users_table = read_csv('usuarios.csv')

    return users_table.loc[users_table['usuario'] == username, 'hash_pwd'].values[0]


def recuperaSenhaUsuario(email: str):
    """Gera um código de recuperação de senha e envia para o e-mail do usuário cadastrado"""
    response = requests.post(url=random_api_url, json=random_api_request_body).json()
    
    #Lista de 6 dígitos
    random_list = response['result']['random']['data']

    #Envia um e-mail para o usuário com o código de recuperação

    #Configura variáveis de e-mail
    email_sender = conta_email
    email_password = gmail_app_pwd
    email_receiver = email
    subject = 'Recuperação de senha de acesso - Jopy Senhas'
    body = f"""
    Olá!

    Use o código abaixo para recuperar sua senha no Jopy Senhas:


    """

    for number in random_list:
        body = body + str(number)

    

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    em.set_content(body)
    context = ssl.create_default_context()

    #Envia o e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def criaNovoLogin(dono_senha, dominio, usuario, senha):
    """Função que cria um objeto do tipo login com dados fornecidos pelo usuário logado"""
    return classes.Login(dono_senha=dono_senha, dominio=dominio, usuario=usuario, senha=senha)


def salvaLogin(Login: Login):
    """Função que salva um objeto do tipo login no arquivo csv"""
    
    #Cria uma lista de valores a partir dos atributos do objeto login
    atributos = [value for value in vars(Login).values()]
    
    with open('senhas.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(atributos)


def geraMenu():
    """Gera um menu para interação com o usuário na tela
    Caso o usuário escolha uma opção válida, retorna o valor inteiro da opção escolhida
    Caso contrário, repete as mensagens de menu"""
    digito_valido = False

    while digito_valido == False:
        print('\n----------------------------------------------')
        print('Bem vindo ao programa gerenciador de senhas')
        print('Digite 0 para sair do programa')
        print('Digite 1 para cadastrar um novo usuário')
        print('Digite 2 para logar caso já tenha uma conta')
        print('------------------------------------------------\n')
    
        digito_inserido = input('Digite a opção desejada: \n')
        
        #Testa se o valor inserido pelo usuário é válido
        if str.isdigit(digito_inserido):
            #Se o dígito inserido for um número, convrete a variável dígito inserido para o tipo inteiro
            digito_inserido = int(digito_inserido)
            if digito_inserido in range(3):
                digito_valido = True
                return int(digito_inserido)

        #O código só chega aqui se o teste acima, para valores inteiros válidos, não for validado
        print('\n Dígito inválido. Insira uma opção válida. \n')


def avalia_opcao(opcao: int):
    """Avalia a opção inserida pelo usuário, e executa a ação correspondente
    Retorna um objeto Login caso a opção escolhida seja 1
    Retorna 0 caso o usuário tenha escolhido sair do programa"""
    match opcao:
        case 0:
            print('Programa encerrado! Até breve!')
            return 0
        case 1:
            print('\nVamos te cadastrar!')
            nome_usuario = input('Digite um nome de usuário: \n')

            #Verifica se o usuário já foi cadastrado:
            if integridade_usuario(username=nome_usuario):
                #I tried using getpass, but it's not popping up in the top of my screen
                #senha = getpass('Digite uma senha:') #Will analyze it later
                
                #Fazendo o hash da senha com o bcrypt
                senha = input('Digite uma senha: \n')
                salt = bcrypt.gensalt()
                senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
                
                #Convert the byte type to string, in order to save the file in the csv
                senha = str(senha)[2:-1]

                #Cadastra o usuário no csv de usuários
                novoUsuario(username=nome_usuario, pwd=senha)
                
            else: #Caso o usuário já esteja cadastrado
                print('\nUsuário já cadastrado!')

            #O valor de retorno 1 redireciona o usuário para a tela de menu
            return 1


        case 2:
            print('Vamos fazer seu login\n')
            nome_usuario = input('Digite seu nome de usuário: \n')

            #Verifica se o usuário já está cadastrado
            if integridade_usuario(username=nome_usuario):
                print('Usuário não cadastrado \n')
            else:
                senha = hash(input(f'Olá, {nome_usuario}! \n Digite sua senha para logar no Jopy Senhas: \n'))

            

            
            return 2


def avalia_opcao_menu2(opcao: int):
    """Avalia a opção inserida por um usuário já cadastrado no segundo menu
    Executa a ação correspondente à opção escolhida
    Retorna um objeto Login caso a opção escolhida seja 1"""

    match opcao:
        case 1:
            dominio = input('Informe o site para o qual deseja salvar a senha:\n')
            usuario = input('Informe o login (usuário) da senha:\n')
            senha = input('Informe a senha que deseja salvar:\n')
            
            return Login(dono_senha='usuario_teste', dominio=dominio, usuario=usuario, senha=senha)
        

#Ambiente de testes
if __name__ == '__main__':
    senha_resultado = obtem_senha_usuario(username='pteixeira').encode('utf-8')
    senha_teste1 = 'Senha123'
    
    if bcrypt.checkpw(senha_teste1.encode('utf-8'), senha_resultado):
          print('Senhas iguais!\nProcesso de hashing bem sucedido')
    else:
          print('hash não funcionou. Senhas não bateram.')
    