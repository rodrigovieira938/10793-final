class Utilizador: #Para o utilizador são precisos estes campos: nome, id, telefone, email, morada, idade
    def __init__(self, nome : str, id : int, telefone: str, email : str, morada : str, idade: int, is_user: bool):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.morada = morada
        self.idade = idade
        self.aulas = []
        self.is_user = is_user
