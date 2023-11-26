class Login:
    """Classe que representa uma senha salva no sistema de gerenciamento de senhas"""
    
    def __init__(self, dono_senha, dominio, usuario, senha):
        self.dono_senha = dono_senha
        self.dominio = dominio
        self.usuario = usuario
        self.senha = senha
