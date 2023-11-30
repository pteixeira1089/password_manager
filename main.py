"""Arquivo que executa a lógica do gerenciador de senhas"""
import gerenciador_senhas_funcoes as functions


#Testa se já há um arquivo csv criado para armazenar senhas
if not(functions.verificaRegistroSenhas()):
    functions.criaArquivoSenhas()

#Testa se já há um arquivo csv criado para armazenar usuários
if not(functions.verificaRegistroUsuarios()):
    functions.criaArquivoUsuarios()

#Testa se já há um arquivo csv criado para armazenar tentativas de recuperação de senha
if not(functions.verificaRegistroRecuperacaoUsuarios()):
    functions.criaArquivoLogRecuperacaoUsuarios()

#Chama o menu de interação
opcao = functions.geraMenu()

#Avalia a opção inserida
resultado = functions.avalia_opcao(opcao=opcao)

#Se o resultado for 1, mostra dados da senha cadastrada
if resultado == 1:
    print('Usuário cadastrado com sucesso!')
