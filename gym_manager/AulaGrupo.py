from .Utilizador import Utilizador
import datetime

class Aulasgrupo:
    def __init__(self,nome:str, id : int, instrutor : Utilizador, horainicio: datetime.datetime, horafinal: datetime.datetime, limit):
        self.nome = nome
        self.id = id
        self.instrutor = instrutor
        self.horainicio = horainicio
        self.horafinal = horafinal
        self.limit = limit
        self.alunos = []