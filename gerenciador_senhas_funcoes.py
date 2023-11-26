"""Arquivo de funções que são utilizadas no programa principal"""
import os
import csv
import sys
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
                sys.exit('Programa encerrado')
            case '1':
                digito_valido = True
                return int(digito_inserido)
            case _:
                digito_valido = False
                print('\n Dígito inválido. Insira uma opção válida. \n')


def avalia_opcao(opcao: int):
    """Avalia a opção inserida pelo usuário, e executa a ação correspondente
    Retorna um objeto senha caso a opção escolhida for válida
    Retorna False se a opção escolhida for inválida"""
    match opcao:
        case 1:
            dominio = input('Informe o site para o qual deseja salvar a senha:\n')
            usuario = input('Informe o login (usuário) da senha:\n')
            senha = input('Informe a senha que deseja salvar:\n')
            
            return Login(dono_senha='usuario_teste', dominio=dominio, usuario=usuario, senha=senha)


        
        case _:
            print('Opção inválida')
            
            return False

