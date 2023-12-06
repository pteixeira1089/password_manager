"""Arquivo que executa a lógica do gerenciador de senhas"""
from procedures import RegisterNewUser, SendRecoveryCode, NewPwdRecoveryLog
import gerenciador_senhas_funcoes as functions


# Testa se já há um arquivo csv criado para armazenar senhas
if not (functions.verificaRegistroSenhas()):
    functions.criaArquivoSenhas()

# Testa se já há um arquivo csv criado para armazenar usuários
if not (functions.verificaRegistroUsuarios()):
    functions.criaArquivoUsuarios()

# Testa se já há um arquivo csv criado para armazenar tentativas de recuperação de senha
if not (functions.verificaRegistroRecuperacaoUsuarios()):
    functions.criaArquivoLogRecuperacaoUsuarios()

# Inicia a variável de controle do menu de interação
resultado = None

while resultado != 0:
    # Chama o menu de interação
    opcao = functions.main_menu()

    # Avalia a opção inserida
    match opcao:
        case 0: #code for exiting program
            print('Programa encerrado! Até breve!')
        case 1: #code for registering new user
            RegisterNewUser()
            resultado = None #This ensures the main menu loop is going to repeat
        case 2: #Code for login
            print('Vamos fazer seu login\n')
            usr_name = input('Digite seu nome de usuário:\n')
            typed_pwd = input('Digite sua senha:\n')
            
            log_in_result_code = functions.log_in_user(usr_name=usr_name, typed_pwd=typed_pwd)

            match log_in_result_code:
                case 0: #Code for invalid user name
                    print('Usuário não cadastrado. Crie um novo usuário ou tente repetir seu login com um nome de usuário diferente.\n')
                case 1: #Code for valid user name, but wrong password
                    wrong_pwd_menu_code = functions.wrong_pwd_menu(usr_name=usr_name)

                    match wrong_pwd_menu_code: #3 Possible results
                        case 0: #Code for terminating program
                            resultado = 0 #The main loop control variable - if 0, exits the main loop
                        case 1: #Go back to main menu - in this case, the user can try to login again
                            resultado = None #Any value other than 0 restarts the main loop
                        case 2: #Code for run the recovery process
                            
                            #Get user's info in a user object:
                            user = functions.get_usr(usr_name=usr_name)
                            
                            #Generates a pwd recovery code
                            code = functions.generates_pwd_recovery_code()

                            #Sends an email with the generated recovery code to the user
                            SendRecoveryCode(email=user.email_usuario, recovery_code=code)

                            #Creates a recovery log register associated with the user and the generated code
                            NewPwdRecoveryLog(usr_name=usr_name, code=code)
                    
                    #Return None in order to restart the loop of the main menu
                    return None

                case 2: #Code for successful login
                    #Write here the main code of the program
                    print('Oi programador! Você precisa definir o fluxo de seu programa a partar deste ponto considerando como devemos interagir com um usuário logado')
                    
                    #Return None in order to restart the main menu loop
                    return None


  #This block of code executes when exiting the loop
  #Logically, it's equivalent to exiting the program
  print('Programa encerrado! Até a próxima!')