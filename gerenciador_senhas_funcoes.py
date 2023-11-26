"""Arquivo de funções que são utilizadas no programa principal"""
import os
import csv
import sys
from pandas import read_csv
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


def integridade_usuario(username: str):
    """Verifica se existe um usuário cadastrado com o username passado
    Retorna verdadeiro se o usuário não estiver cadastrado
    Retorna false se o usuário já estiver cadastrado"""
    users_table = read_csv('usuarios.csv')
    users = users_table['usuario'].tolist()

    return not(username in users)


def novoUsuario(username: str, pwd: str):
    """Função que cria/registra um novo usuário na tabela de usuários"""



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
        print('Digite 1 para cadastrar uma nova senha')
        print('------------------------------------------------\n')
    
        digito_inserido = input('Digite a opção desejada: \n')

        match digito_inserido:
            case '0':
                digito_valido = True
                return int(digito_inserido)
            case '1':
                digito_valido = True
                return int(digito_inserido)
            case _:
                digito_valido = False
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
            dominio = input('Informe o site para o qual deseja salvar a senha:\n')
            usuario = input('Informe o login (usuário) da senha:\n')
            senha = input('Informe a senha que deseja salvar:\n')
            
            return Login(dono_senha='usuario_teste', dominio=dominio, usuario=usuario, senha=senha)