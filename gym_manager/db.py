import sqlite3
from .Utilizador import Utilizador
from .AulaGrupo import Aulasgrupo
import datetime

class Db:
    def __init__(self):
        try:
            self.sqliteConnection = sqlite3.connect('dados.db')
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    telefone INT,
                    email VARCHAR(255),
                    morada TEXT,
                    idade INT
                );                                               
            ''')
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Instrutores(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    telefone INT,
                    email VARCHAR(255),
                    morada TEXT,
                    idade INT
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Aulasgrupo(
                    nome TEXT,
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    limite_alunos INTEGER,
                    instrutor INTEGER,
                    horainicio VARCHAR(255),
                    horafinal VARCHAR(255)
                );   
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Inscricoes(
                  id_aula INTEGER,
                  id_aluno INTEGER
                );
            """)
           
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro', error) 
              
    def CriarAluno(self, nome, telefone, email, morada, idade):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("INSERT INTO Alunos (nome, telefone, email, morada, idade) VALUES (?,?,?,?,?)", 
                           (nome, telefone, email, morada, idade))
            cursor.execute("SELECT last_insert_rowid()")
            self.sqliteConnection.commit()
            return cursor.fetchone()[0]
        except sqlite3.Error as error:
            print('Ocorreu um erro ao criar utilizador: ', error)
    def CriarInstrutor(self, nome, telefone, email, morada, idade):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("INSERT INTO Instrutores (nome, telefone, email, morada, idade) VALUES (?,?,?,?,?)", 
                           (nome, telefone, email, morada, idade))
            cursor.execute("SELECT last_insert_rowid()")
            self.sqliteConnection.commit()
            return cursor.fetchone()[0]
        except sqlite3.Error as error:
            print('Ocorreu um erro ao criar o Instrutor', error)
    def CriarAulaDeGrupo(self,nome:str, instrutor : Utilizador, horainicio, horafinal, limit):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                INSERT INTO Aulasgrupo (nome, instrutor, horainicio, horafinal, limite_alunos) VALUES (?,?,?,?,?)            
            ''', (nome, instrutor.id, horainicio, horafinal, limit))
            cursor.execute("SELECT last_insert_rowid()")
            self.sqliteConnection.commit()
            return cursor.fetchone()[0]
        except sqlite3.Error as error:
            print('Ocorreu um erro ao criar as Aulas', error)
    def AdicionarAlunoAaAula(self,aluno : Utilizador, aula : Aulasgrupo):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('INSERT INTO Inscricoes (id_aula, id_aluno) VALUES (?, ?)', (aula.id, aluno.id))
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro ao adicionar utilizador à aula', error)
    
    def ListarAlunos(self) ->  list[Utilizador]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("""SELECT * FROM Alunos""")
            self.sqliteConnection.commit()
            raw_alunos = cursor.fetchall()
            
            alunos = []
            for aluno in raw_alunos:
                alunos.append(Utilizador(aluno[1], aluno[0], aluno[2], aluno[3], aluno[4], aluno[5], True))
            return alunos
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar alunos', error)
    def ListarInstrutores(self) -> list[Utilizador]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("""SELECT * FROM Instrutores""")
            self.sqliteConnection.commit()
            raw_instrutores = cursor.fetchall()
            
            instrutores = []
            for instrutor in raw_instrutores:
                instrutores.append(Utilizador(instrutor[1], instrutor[0], instrutor[2], instrutor[3], instrutor[4], instrutor[5], False))
            return instrutores
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar instrutores', error)
    def ListarAulaDeGrupo(self) -> list[Aulasgrupo]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("""SELECT * FROM Aulasgrupo""")
            self.sqliteConnection.commit()
            raw_aulas = cursor.fetchall()
            
            aulas = []
            for aula in raw_aulas:
                aulas.append(Aulasgrupo(aula[0],aula[1],self.ProcurarInstrutorID(aula[3]),datetime.datetime.strptime(aula[4], "%d/%m/%Y %H:%M"), datetime.datetime.strptime(aula[5], "%d/%m/%Y %H:%M"), aula[2]))
            return aulas
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar aulas de grupo', error)
    def ListartAulaDeInstrutor(self, instrutor : Utilizador) -> list[Aulasgrupo]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("SELECT * FROM Aulasgrupo where instrutor = ?", (instrutor.id,))
            self.sqliteConnection.commit()
            raw_aulas = cursor.fetchall()
            
            aulas = []
            for aula in raw_aulas:
                aulas.append(Aulasgrupo(aula[0], aula[1],self.ProcurarInstrutorID(aula[3]),datetime.datetime.strptime(aula[4], "%d/%m/%Y %H:%M"), datetime.datetime.strptime(aula[5], "%d/%m/%Y %H:%M"), aula[2]))
            return aulas
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar aulas de grupo', error)
    def ListarIncricoesDeAluno(self, aluno : Utilizador) -> list[Aulasgrupo]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("SELECT * FROM Inscricoes WHERE id_aluno = ?", (aluno.id,))
            self.sqliteConnection.commit()
            inscricoes = cursor.fetchall()
            aulas = []
            for (id_aula, _) in inscricoes:
                aulas.append(self.ProcurarAulaID(id_aula))
            return aulas
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar inscrições de um aluno', error)
    def ListarInscricoesDeAula(self, aula : Aulasgrupo) -> list[Utilizador]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("SELECT * FROM Inscricoes WHERE id_aula = ?", (aula.id,))
            self.sqliteConnection.commit()
            inscricoes = cursor.fetchall()
            aulas = []
            for (_, id_alunos) in inscricoes:
                aulas.append(self.ProcurarAlunoID(id_alunos))
            return aulas
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar inscrições de um aluno', error)
    
    def ProcurarAlunoID(self, id) -> Utilizador:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('SELECT * FROM Alunos WHERE id = ?', (id,))
            raw_instrutor = cursor.fetchone()
            if(raw_instrutor == None):
                return None
            return Utilizador(raw_instrutor[1], raw_instrutor[0], raw_instrutor[2], raw_instrutor[3], raw_instrutor[4], raw_instrutor[5], True)
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)
    def ProcurarInstrutorID(self, id) -> Utilizador:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('SELECT * FROM Instrutores WHERE id = ?', (id,))
            raw_instrutor = cursor.fetchone()
            if(raw_instrutor == None):
                return None
            return Utilizador(raw_instrutor[1], raw_instrutor[0], raw_instrutor[2], raw_instrutor[3], raw_instrutor[4], raw_instrutor[5], False)
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)
    def ProcurarAulaID(self, id) -> Aulasgrupo:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('SELECT * FROM Aulasgrupo WHERE id = ?', (id,))
            raw_aula = cursor.fetchone()
            if(raw_aula == None):
                return None
            return Aulasgrupo(raw_aula[0], raw_aula[1],self.ProcurarInstrutorID(raw_aula[3]),datetime.datetime.strptime(raw_aula[4], "%d/%m/%Y %H:%M"), datetime.datetime.strptime(raw_aula[5], "%d/%m/%Y %H:%M"), raw_aula[2])
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)