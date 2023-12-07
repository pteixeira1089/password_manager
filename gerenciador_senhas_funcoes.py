"""Arquivo de funções que são utilizadas no programa principal"""
import os
import csv
import datetime
import bcrypt  # Pacote que faz o hash das senhas de usuário salvas
import ssl  # Pacote que adiciona camada de segurança para comunicações em rede
import smtplib  # Pacote para envio de e-mails
from email.message import EmailMessage
# from getpass import getpass #I tried using getpass, but it didn't work - the popup didn't show in the top of the screen
import requests
from pandas import read_csv
from keys import conta_email, gmail_app_pwd
from models import random_api_url, random_api_request_body
from gerenciador_senhas_classes import Login, User


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
        writer.writerow(["usuario", "time_stamp_solicitacao",
                        "time_stamp_limite", "codigo"])


def get_usr(usr_name: str):
    """Get a User object from the csv file that corresponds to the given user_name given"""
    users_table = read_csv('usuarios.csv')

    user_pwd = users_table.loc[users_table['usuario']
                               == usr_name, 'hash_pwd'].values[0]
    user_email = users_table.loc[users_table['usuario']
                                 == usr_name, 'email'].values[0]
    user_cpf = users_table.loc[users_table['usuario']
                               == usr_name, 'cpf'].values[0]

    return User(nome_usuario=usr_name, email_usuario=user_email, pwd_hash_usuario=user_pwd, cpf_usuario=user_cpf)


def hash_password(password: str):
    """Hashes a given password using bcrypt
    Returns a string value ready to be written to a csv file
    """

    # Generates a salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_password = bcrypt.hashpw(
        password=password.encode('utf-8'), salt=salt)

    # Convert the byte type to string, in order to save the file in the csv
    return str(hashed_password)[2:-1]


def integridade_usuario(username: str):
    """Verifica se existe um usuário cadastrado com o username passado
    Retorna verdadeiro se o usuário não estiver cadastrado
    Retorna false se o usuário já estiver cadastrado"""
    users_table = read_csv('usuarios.csv')
    users = users_table['usuario'].tolist()

    return not (username in users)


def generates_pwd_recovery_code():
    """Requests a random 6-digit code using Random.Org API"""
    response = requests.post(
        url=random_api_url, json=random_api_request_body).json()

    #Get the 6-digit code from the response
    random_list = response['result']['random']['data']

    # Initiates a variable that will store the generated code
    code = ''

    #iterates the numbers in the generated list from the request
    #Builds a string with the generated numbers
    for number in random_list:
        code = code + str(number)

    return code


def criaNovoLogin(dono_senha, dominio, usuario, senha):
    """Função que cria um objeto do tipo login com dados fornecidos pelo usuário logado"""
    return classes.Login(dono_senha=dono_senha, dominio=dominio, usuario=usuario, senha=senha)


def salvaLogin(Login: Login):
    """Função que salva um objeto do tipo login no arquivo csv"""

    # Cria uma lista de valores a partir dos atributos do objeto login
    atributos = [value for value in vars(Login).values()]

    with open('senhas.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(atributos)


def main_menu():
    """
    Generates the main menu of the program
    Returns the option selected by the user:
    0 - in case the user wants to exit the program
    1 - In case the user wants to register a new user
    2 - In case the user wants to login
    3 - In case the user wants to redefine password using a recovery code
    """
    digito_valido = False
    number_of_options = 4  # 4 options available to choose

    while digito_valido == False:
        print('\n----------------------------------------------')
        print('Bem vindo ao programa gerenciador de senhas')
        print('Digite 0 para sair do programa')
        print('Digite 1 para cadastrar um novo usuário')
        print('Digite 2 para logar caso já tenha uma conta')
        print('Digite 3 para redefinir sua senha usando um código recebido')
        print('------------------------------------------------\n')

        digito_inserido = input('Digite a opção desejada: \n')

        # Testa se o valor inserido pelo usuário é válido
        if str.isdigit(digito_inserido):
            # Se o dígito inserido for um número, convrete a variável dígito inserido para o tipo inteiro
            digito_inserido = int(digito_inserido)
            if digito_inserido in range(number_of_options):
                digito_valido = True
                return int(digito_inserido)

        # O código só chega aqui se o teste acima, para valores inteiros válidos, não for validado
        print('\n Dígito inválido. Insira uma opção válida. \n')


def wrong_pwd_menu(usr_name: str):
    """Generates a wrong_password options menu for a given user identified by its user name
    Returns 3 possibile results
    0 - in case the user wants to exit the program
    1 - in case the user wants to go back to main menu
    2 - in case the user wants to run a recovery password process
    """
    digito_valido = False
    number_of_options = 3

    while digito_valido == False:
        print('\n----------------------------------------------')
        print(f'Olá {usr_name}! Você digitou a senha errada para seu usuário. Escolha uma das opções abaixo para continuar:')
        print('Digite 0 para sair do programa')
        print('Digite 1 para voltar ao menu principal')
        print('Digite 2 caso tenha esquecido sua senha e queira recuperá-la')
        print('------------------------------------------------\n')

        digito_inserido = input('Digite a opção desejada: \n')

        # Testa se o valor inserido pelo usuário é válido
        if str.isdigit(digito_inserido):
            # Se o dígito inserido for um número, converte a variável dígito inserido para o tipo inteiro
            digito_inserido = int(digito_inserido)
            if digito_inserido in range(number_of_options):
                digito_valido = True
                return int(digito_inserido)

        # O código só chega aqui se o teste acima, para valores inteiros válidos, não for validado
        print('\n Dígito inválido. Insira uma opção válida. \n')


def recover_pwd_menu():
    """Gera um menu para interação com o usuário que está tentando recuperar sua senha
    Caso o usuário escolha uma opção válida, retorna o valor inteiro da opção escolhida
    Caso contrário, repete as mensagens de menu"""
    digito_valido = False
    qtd_opcoes = 3

    while digito_valido == False:
        print('\n----------------------------------------------')
        print('Menu de recuperação de senha:')
        print('Digite 0 para sair do programa')
        print('Digite 1 para digitar o código de recuperação recebido')
        print('Digite 2 para receber um novo código de recuperação')
        print('------------------------------------------------\n')

        digito_inserido = input('Digite a opção desejada: \n')

        # Testa se o valor inserido pelo usuário é válido
        if str.isdigit(digito_inserido):
            # Se o dígito inserido for um número, converte a variável dígito inserido para o tipo inteiro
            digito_inserido = int(digito_inserido)
            if digito_inserido in range(qtd_opcoes):
                digito_valido = True
                return int(digito_inserido)

        # O código só chega aqui se o teste acima, para valores inteiros válidos, não for validado
        print('\n Dígito inválido. Insira uma opção válida. \n')


def evaluate_recovery_code(usr_name: str, typed_code: str):
    """
    Receives the user name and a recovery code
    Returns 0 if the user doesn't have a recovery process registered on log
    Returns 1 for expired recovering code
    Returns 2 for wrong recovery code
    Returns 3 for right recovery code
    """
    #Reads the recovery password log
    recovery_log = read_csv('log_recuperacao_senha.csv')
    
    #Get the users with registered recovery logs
    recovery_log_users_list = recovery_log['usuario'].to_list()

    if not(usr_name in recovery_log_users_list):
        return 0

    # Find the user corresponding data in recovery pwd register
    user_time_stamp_limit = recovery_log.loc[recovery_log['usuario'] == usr_name, 'time_stamp_limite'].values[0]
    user_time_stamp_limit = datetime.datetime.strptime(user_time_stamp_limit, '%Y-%m-%d %H:%M:%S.%f')
    user_recovery_code = recovery_log.loc[recovery_log['usuario'] == usr_name, 'codigo'].values[0]

    #Converts user_recovery_code to string type
    user_recovery_code = user_recovery_code.astype(str)

    if datetime.datetime.now() > user_time_stamp_limit:
        return 1

    if typed_code != user_recovery_code:
        return 2
    
    #In case the function didn't return any of above codes, it means the typed recovery code is correct and
    #not expired - returns 3
    return 3
                

def evaluates_option_wrong_password_menu(option: int, usr_name: str):
    """Evaluates the option chosen by the user in 'wrong pwd menu'
    and executes the corresponding action"""
    match option:
        case 0:
            print('Programa encerrado! Até breve!')
            return 0
        case 1:
            if check_password(usr_name=usr_name):
                # 3 returned code stands for passing for logged-in user menu
                return 3
            else:
                # 1 Stands for wrong typed password
                return 1
        case 2:

            # Maybe this block of code should be on the logical part of the code - the main
            # Or inside a procedure that could be called inside the main
            # Because I think the code would be more understandable if the function only return values
            # This structure could eliminate the number of functions in this program - I'd eliminate the 'evaluate_option_[menu_name]' functions
            print('Um código de recuperação foi enviado para seu e-mail')
            user = get_usr(usr_name)

            # Envia um e-mail com código de recuperação de senha ao usuário cadastrado
            # E armazena o código gerado no processo de recuperação na variável code
            code = generates_pwd_recovery_code(user.email_usuario)

            # Generates current time, time limit and limit time to complete the recovery process
            current_time = datetime.datetime.now()
            time_limit = datetime.timedelta(minutes=5)
            limit_time = current_time + time_limit

            recover_entry = [usr_name, current_time, limit_time, code]

            # Creates an entry on log_recuperacao_senha.csv
            with open('log_recuperacao_senha.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(recover_entry)

            return 2  # code 2 stands for recovery code sent to the user


def check_password(usr_name: str, typed_pwd: str):
    """Provided a user name and a typed_pwd, this function gets it's stored password
    And compares it with the typed_pwd
    Returns true if typed password equals stored password
    Returns false otherwise"""

    # Gets an user object from the given usr_name
    user = get_usr(usr_name=usr_name)

    # Gets the user's stored password
    stored_pwd = user.pwd_hash_usuario.encode('utf-8')

    # Asks the user to type his password
    byte_typed_pwd = typed_pwd.encode('utf-8')

    # Tests if the typed pwd equals the registered pwd
    return bcrypt.checkpw(byte_typed_pwd, stored_pwd)


def avalia_opcao_menu_principal(opcao: int):
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

            # Verifica se o usuário já foi cadastrado:
            if integridade_usuario(username=nome_usuario):
                # I tried using getpass, but it's not popping up in the top of my screen
                # senha = getpass('Digite uma senha:') #Will analyze it later

                # Fazendo o hash da senhat
                senha = input('Digite uma senha: \n')
                senha = hash_password(password=senha)

                # Cadastra o usuário no csv de usuários
                novoUsuario(username=nome_usuario, pwd=senha)

            else:  # Caso o usuário já esteja cadastrado
                print('\nUsuário já cadastrado!')

            # O valor de retorno 1 redireciona o usuário para a tela de menu
            return 1

        case 2:
            print('Vamos fazer seu login\n')
            nome_usuario = input('Digite seu nome de usuário: \n')

            # Verifica se o usuário já está cadastrado
            if integridade_usuario(username=nome_usuario):
                print('Usuário não cadastrado \n')
                print('Você será redirecionado para o menu principal\n')
            else:
                if check_password(usr_name=nome_usuario):
                    # Code 3 stands for passing to the loogged-in user menu
                    return 3
                else:
                    # Calls wrong password menu
                    wrong_pwd_menu(nome_usuario)
                    return 2  # Stands for wrong password


def avalia_opcao_menu2(opcao: int):
    """Avalia a opção inserida por um usuário já cadastrado no segundo menu
    Executa a ação correspondente à opção escolhida
    Retorna um objeto Login caso a opção escolhida seja 1"""

    match opcao:
        case 1:
            dominio = input(
                'Informe o site para o qual deseja salvar a senha:\n')
            usuario = input('Informe o login (usuário) da senha:\n')
            senha = input('Informe a senha que deseja salvar:\n')

            return Login(dono_senha='usuario_teste', dominio=dominio, usuario=usuario, senha=senha)


def log_in_user(usr_name: str, typed_pwd: str):
    """Given a usr_name, tries to log him in
    There are 3 possible results:
    0 - Invalid user name;
    1 - Valid user name, but wrong password
    2 - Successfull log in
    """

    # Tests if the user is already registered
    if integridade_usuario(usr_name):
        return 0

    # Tests if the typed password matches the registered password
    if check_password(usr_name=usr_name, typed_pwd=typed_pwd):
        return 2
    else:  # Didn't need this else, but it's presence makes the code more readable
        return 1