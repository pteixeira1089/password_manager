import datetime
import ssl  # Pacote que adiciona camada de segurança para comunicações em rede
import smtplib  # Pacote para envio de e-mails
from email.message import EmailMessage
from gerenciador_senhas_funcoes import integridade_usuario, novoUsuario, get_usr, generates_pwd_recovery_code
# Personal variables - used in API's and other configurations
from keys import conta_email, gmail_app_pwd


def RegisterNewUser():
    """Procedure that registers new user"""
    print('\nVamos te cadastrar!')
    nome_usuario = input('Digite um nome de usuário: \n')

    # Verifica se o usuário já foi cadastrado:
    if integridade_usuario(username=nome_usuario):
        senha = input('Digite uma senha: \n')
        senha = hash_password(password=senha)

        # Cadastra o usuário no csv de usuários
        novoUsuario(username=nome_usuario, pwd=senha)

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