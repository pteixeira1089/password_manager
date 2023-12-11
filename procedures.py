import datetime
import csv
from pandas import read_csv
import ssl  # Pacote que adiciona camada de segurança para comunicações em rede
import smtplib  # Pacote para envio de e-mails
from email.message import EmailMessage

#These are the imports necessary to crypt strings
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib #used to generate a 23-byte hash value of the string

# Program functions
from gerenciador_senhas_funcoes import integridade_usuario, hash_password
# Personal variables - used in API's and other configurations
from keys import conta_email, gmail_app_pwd


def criaArquivoSenhas():
    """This procedure creates a passwords file"""
    with open('senhas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["dono_senha", "nome_servico", "dominio", "descricao", "login", "senha", "iv"])


def criaArquivoUsuarios():
    """Função que inicializa um arquivo de usuários com o nome 'usuarios.csv'"""
    with open('usuarios.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["usuario", "email", "hash_pwd", "key"])


def criaArquivoLogRecuperacaoUsuarios():
    """Função que inicializa um arquivo de log de recuperação de senhas de usuário com o nome 'log_recuperacao_senha.csv'"""
    with open('log_recuperacao_senha.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["usuario", "time_stamp_solicitacao",
                        "time_stamp_limite", "codigo"])


def clearExpiredRecoveryRequests():
    """
    Clears all expired recovery requests on the recovery log
    """
    
    #Reads the csv to a pandas dataframe
    recovery_requests = read_csv('log_recuperacao_senha.csv')

    #Get now time in string format
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S.%f')

    #Drops all rows where 'time_stamp_limite' is less than now
    recovery_requests = recovery_requests.drop(recovery_requests.loc[recovery_requests['time_stamp_limite'] < now].index)

    #Exports the dataframe again
    recovery_requests.to_csv('log_recuperacao_senha.csv', index=False)


def clearRecoveryRequests(usr_name: str):
    """
    Clear all recovery requests of the given user from the recovery requests log
    """
    recovery_requests = read_csv('log_recuperacao_senha.csv')

    recovery_requests = recovery_requests.loc[recovery_requests['usuario'] != usr_name]

    recovery_requests.to_csv('log_recuperacao_senha.csv', index=False)


def RegisterNewUser():
    """Procedure that registers new user"""
    print('\n \nVamos te cadastrar!')
    nome_usuario = input('\nDigite um nome de usuário: \n')
    
    if integridade_usuario(username=nome_usuario):
        typed_pwd = input('\nDigite uma senha: \n')
        typed_pwd = hash_password(password=typed_pwd)

        email = input('\nDigite um email válido:\n')

        #Generates a encryption key for the user
        #We will use a 32 byte version of the hashed user_name to generate a salt for the key
        encoded_usr_name = nome_usuario.encode('utf-8') #Encode the pwd to bytes
        salt = hashlib.sha256(encoded_usr_name).digest() #Uses sha-256 method to get a fixed lenght string from the given pwd

        #Truncate to 32 bytes - ensures the value will have 32 bytes long
        salt = salt[:32]

        #Generates a key
        usr_key = PBKDF2(password=typed_pwd, salt=salt, dkLen=32)

        #Prepares the key to be registered as a string on the csv file
        usr_key = str(usr_key)

        #Prepares a list to be used as data entry to the users csv file
        user_list = [nome_usuario, email, typed_pwd, usr_key]

        #Register the values on the csv
        with open('usuarios.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(user_list)

        print(f'\nUsuário {nome_usuario} registrado com sucesso!\n')

    else:  # Caso o usuário já esteja cadastrado
        print('\nUsuário já cadastrado!')


def SendRecoveryCode(email: str, recovery_code: str):
    """Sends a password recovery code to a given email"""

    # e-mail variables
    email_sender = conta_email
    email_password = gmail_app_pwd
    email_receiver = email
    subject = 'Recuperação de senha de acesso - Jopy Senhas'
    body = f"""
    Olá!

    Use o código abaixo para recuperar sua senha no Jopy Senhas:

    {recovery_code}
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    em.set_content(body)
    context = ssl.create_default_context()

    # Sends the mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def NewPwdRecoveryLog(usr_name:str, code: str):
    """
    Creates a new recovery log to the password recovery log
    """

    #Generates current time, time limit and limit time to complete the recovery process
    current_time = datetime.datetime.now()
    time_limit = datetime.timedelta(minutes=5)
    limit_time = current_time + time_limit

    #Prepares a list to be used as entry data on the csv file
    recover_entry = [usr_name, current_time, limit_time, code]

    # Creates an entry on log_recuperacao_senha.csv
    with open('log_recuperacao_senha.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(recover_entry)


def UpdateUserPwd(usr_name: str, new_pwd: str):
    # Reads users csv file
    users_table = read_csv('usuarios.csv')

    #Sets the new pwd to the corresponding register
    users_table.loc[users_table['usuario'] == usr_name, 'hash_pwd'] = new_pwd

    #Exports the dataframe back to csv
    users_table.to_csv('usuarios.csv', index=False)


if __name__ == '__main__':
    clearExpiredRecoveryRequests()