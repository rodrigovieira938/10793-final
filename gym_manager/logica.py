from .db import Db
from .Utilizador import Utilizador
from .AulaGrupo import Aulasgrupo
import datetime

class Logica:
    def __init__(self):
        self.db = Db()
    def CriarUtilizador(self, nome : str, telefone : str, email : str, morada : str, idade : int):
        user = Utilizador(nome, 0, telefone, email, morada, idade, True)
        user.id = self.db.CriarAluno(nome, telefone, email, morada, idade) #CriarUtilizador deve retornar a id
        return user
    def CriarInstructor(self, nome : str, telefone : str, email : str, morada : str, idade : int):
        user = Utilizador(nome, 0, telefone, email, morada, idade, False)
        user.id = self.db.CriarInstrutor(nome, telefone, email, morada, idade) #CriarUtilizador deve retornar a id
        return user
    def CriarAulaDeGrupo(self,nome: str, instrutor : Utilizador, horainicio : datetime.datetime, horafinal : datetime.datetime, limit : int):  # um instrutor não pode dar mais de uma aula em simultâneo 
        aula = Aulasgrupo(nome, None, instrutor, horainicio, horafinal, limit)
        
        for al in self.db.ListartAulaDeInstrutor(instrutor):
            if aula.horainicio <= al.horafinal and al.horafinal <= aula.horafinal:
                return False
        
        aula.id = self.db.CriarAulaDeGrupo(nome, instrutor, horainicio.strftime("%d/%m/%Y %H:%M"), horafinal.strftime("%d/%m/%Y %H:%M"), limit)
        return aula
    def AdicionarAlunoAaAula(self,utilizador, aula : Aulasgrupo) -> bool:  # Não se pode inscrever em mais de uma aula no mesmo horário, Não se pode inscrever em aulas já lotadas
        for al in self.db.ListarIncricoesDeAluno(utilizador):
            if aula.horainicio <= al.horafinal and al.horafinal <= aula.horafinal:
                return False
        if len(self.db.ListarInscricoesDeAula(aula))+1 > aula.limit:
            return False  
        self.db.AdicionarAlunoAaAula(utilizador, aula)
        return True