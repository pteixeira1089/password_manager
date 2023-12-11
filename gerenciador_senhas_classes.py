class Login:
    """Classe que representa uma senha salva no sistema de gerenciamento de senhas"""
    
    def __init__(self, dono_senha: str, nome_servico: str, dominio: str, descricao: str, login: str, senha: str, iv: str):
        self.dono_senha = dono_senha
        self.nome_servico = nome_servico
        self.dominio = dominio
        self.descricao = descricao
        self.login = login
        self.senha = senha
        self.iv = iv

class User:
    """Representa um usuário do sistema"""

    def __init__(self, nome_usuario: str, email_usuario: str, pwd_hash_usuario: str, key: str):
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.pwd_hash_usuario = pwd_hash_usuario
        self.key = key


class RecoveryRequest:
    """Stands for a recovery request"""

    def __init__(self, usr_name: str, request_time_stamp: str, request_time_limit: str, request_code: str):
        self.usr_name = usr_name
        self.request_time_stamp = request_time_stamp
        self.request_time_limit = request_time_limit
        self.request_code = request_code