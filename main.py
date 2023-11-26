"""Arquivo que executa a lógica do gerenciador de senhas"""
import os
import gerenciador_senhas_funcoes as functions


#Testa se já há um arquivo csv criado para armazenar senhas
if not(functions.verificaRegistroSenhas()):
    functions.criaArquivoSenhas()

#Chama o menu de interação
opcao = functions.geraMenu()

#Avalia a opção inserida
resultado = functions.avalia_opcao(opcao=opcao)

print(f'O dono da senha é: {resultado.dono_senha}')
print(f'O site para o qual a senha funciona é: {resultado.dominio}')
print(f'O usuário (login) é: {resultado.usuario}')
print(f'A senha registrada é: {resultado.senha}')
