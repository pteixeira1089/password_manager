"""Arquivo que executa a lógica do gerenciador de senhas"""
from procedures import RegisterNewUser, SendRecoveryCode, NewPwdRecoveryLog, UpdateUserPwd, criaArquivoSenhas, criaArquivoUsuarios, criaArquivoLogRecuperacaoUsuarios, clearRecoveryRequests, clearExpiredRecoveryRequests
import gerenciador_senhas_funcoes as functions


# Testa se já há um arquivo csv criado para armazenar senhas
if not (functions.lookup_pwd_file()):
    criaArquivoSenhas()

# Testa se já há um arquivo csv criado para armazenar usuários
if not (functions.lookup_users_file()):
    criaArquivoUsuarios()

# Testa se já há um arquivo csv criado para armazenar tentativas de recuperação de senha
if not (functions.lookup_recovery_user_pwd_log_file()):
    criaArquivoLogRecuperacaoUsuarios()

#Clear expired recovery requests
clearExpiredRecoveryRequests()

# Inicia a variável de controle do menu de interação
resultado = None

while resultado not in [0,1]: #0 Stands for exiting the program, and 1 stands for successful login
    # Chama o menu de interação
    opcao = functions.main_menu()

    # Avalia a opção inserida
    match opcao:
        case 0:  # code for exiting program
            # Sets the loop control variable to 0 in order to exit the main menu loop
            resultado = 0
        case 1:  # code for registering new user
            RegisterNewUser()
            resultado = None  # This ensures the main menu loop is going to repeat
        case 2:  # Code for login
            print('\n\nVamos fazer seu login\n')
            usr_name = input('Digite seu nome de usuário:\n')
            typed_pwd = input('Digite sua senha:\n')

            log_in_result_code = functions.log_in_user(
                usr_name=usr_name, typed_pwd=typed_pwd)

            match log_in_result_code:
                case 0:  # Code for invalid user name
                    print(
                        'Usuário não cadastrado. Crie um novo usuário ou tente repetir seu login com um nome de usuário diferente.\n')
                case 1:  # Code for valid user name, but wrong password
                    wrong_pwd_menu_code = functions.wrong_pwd_menu(
                        usr_name=usr_name)

                    match wrong_pwd_menu_code:  # 3 Possible results
                        case 0:  # Code for terminating program
                            resultado = 0  # The main loop control variable - if 0, exits the main loop
                        case 1:  # Go back to main menu - in this case, the user can try to login again
                            resultado = None  # Any value other than 0 restarts the main loop
                        case 2:  # Code for running the recovery process

                            # Get user's info in a user object:
                            user = functions.get_usr(usr_name=usr_name)

                            #Deletes all recovery entries of the given user
                            #This guarantees each user has always only one recovery request on the log
                            clearRecoveryRequests(usr_name=user)

                            # Generates a pwd recovery code
                            code = functions.generates_pwd_recovery_code()

                            # Sends an email with the generated recovery code to the user
                            SendRecoveryCode(
                                email=user.email_usuario, recovery_code=code)

                            # Creates a recovery log register associated with the user and the generated code
                            NewPwdRecoveryLog(usr_name=usr_name, code=code)

                            print(
                                'Um código de recuperação de senha foi enviado para seu e-mail.')
                            print(
                                'Utilize a opção 3 no menu principal para definir uma nova senha usando o código recebido')

                            # Sets the main menu loop control variable
                            resultado = None  # Any value ther than 0 restarts the main loop

                case 2:  # Code for successful login
                    # Defines the logged_user variable
                    logged_user = usr_name

                    # Sets the result to 1 in order to exit main menu code and to drive the flow to the logged-in user area
                    resultado = 1
        case 3:  # Code for reseting password with recovery code
            usr_name = input('\n\nDigite seu nome de usuário\n')
            received_code = input(
                '\nDigite o código de recuperação que você recebeu em seu e-mail\n')

            recovery_process_result = functions.evaluate_recovery_code(
                usr_name=usr_name, typed_code=received_code)

            match recovery_process_result:
                case 0:  # Code for no existing recovery process
                    print(
                        'Não há solicitação de recuperação de senha para este usuário.')

                    # Set the loop control variable to None in order to repeat main menu
                    opcao = None

                case 1:  # Code for expired recovery code
                    print(
                        'O código de recuperação de senha expirou. Inicie um novo procedimento de reset de senha.')

                    # Set the loop control variable to None in order to repeat main menu
                    opcao = None

                case 2:  # Code for wrong recovery code
                    print('O código de recuperação de senha informado está incorreto.')
                    print('Reinicie o procedimento de recuperação de senha novamente')

                    # Set the loop control variable to None in order to repeat main menu
                    opcao = None

                case 3:  # Code for valid recovery code
                    new_password = input(
                        f'Digite uma nova senha para o usuário {usr_name}:\n')

                    # Hashes the password
                    new_password = functions.hash_password(new_password)

                    # Updates password in the csv file
                    UpdateUserPwd(usr_name=usr_name, new_pwd=new_password)

                    # Tells the result to the user
                    print(
                        'Senha atualizada com sucesso! Faça login com sua nova senha no menu principal.')

                    # Set the loop control variable to None in order to repeat main menu
                    opcao = None



#The following flow repeats while the control variable is set to 1, which means a successful logged user
while resultado == 1:
    #Shows logged user menu
    option = functions.logged_user_menu(logged_usr_name=logged_user)
    
    print(f'Você escolheu a opção {option}')

    #I'm using this variable to force the exit of the program
    #It'll vanish in the released version
    resultado = 0


# This block of code executes when exiting all the loops
# Logically, it's equivalent to exiting the program
print('Programa encerrado! Até a próxima!')

