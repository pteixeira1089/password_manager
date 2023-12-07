class Login:
    """Classe que representa uma senha salva no sistema de gerenciamento de senhas"""
    
    def __init__(self, dono_senha, dominio, usuario, senha):
        self.dono_senha = dono_senha
        self.dominio = dominio
        self.usuario = usuario
        self.senha = senha

class User:
    """Representa um usuário do sistema"""

    def __init__(self, nome_usuario: str, email_usuario: str, pwd_hash_usuario: str, cpf_usuario: str):
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.pwd_hash_usuario = pwd_hash_usuario
        self.cpf_usuario = cpf_usuario
