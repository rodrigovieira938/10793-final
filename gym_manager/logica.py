class Utilizador: #Para o utilizador são precisos estes campos: nome, id, telefone, email, morada, idade
    def __init__(self, nome, id, telefone, email, morada, idade):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.morada = morada
        self.idade = idade
        self.aulas = []

class Instrutor:
    def __init__(self, nome, id, telefone, email, morada, idade):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.morada = morada
        self.idade = idade
        self.aulasinsc = []
class Aulasgrupo:
    def __init__(self, instrutor, horainicio, horafinal, limit):
        self.instrutor = instrutor
        self.horainicio = horainicio
        self.horafinal = horafinal
        self.limit = 10
        self.alunos = []
class Logica:
    def CriarUtilizador(self, nome, telefone, email, morada, idade):
        utilizador = Utilizador(nome, 0, telefone, email, morada, idade)
        return utilizador
    def CriarInstructor(self,nome, telefone, email, morada, idade):
        instrutor = Instrutor(nome,0, telefone, email, morada, idade)
        return instrutor
    def CriarAulaDeGrupo(self,instructor, horainicio, horafinal):  # um instrutor não pode dar mais de uma aula em simultâneo 
        aulagrupo = Aulasgrupo(instructor, horainicio, horafinal)
        for aula in instructor.aulasinsc:
            if aula.horainicio >= horainicio and aula.horafinal <= horafinal:
                return None
        return aulagrupo
    def AdicionarUtilizadorAAula(self,utilizador, aula):  # Não se pode inscrever em mais de uma aula no mesmohorário, Não se pode inscrever em aulas já lotadas
        utilizadoraula = Aulasgrupo(utilizador,aula)
        for aula in utilizador.aulasinsc:
            if aula.horainicio >= utilizadoraula.horainicio and aula.horafinal <= utilizadoraula.horafinal:
                 return None
            if utilizadoraula.alunos == utilizadoraula.limit:
                return None
            return utilizadoraula
