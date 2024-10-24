import sqlite3
from .logica import Utilizador, Instrutor, Aulasgrupo
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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    limite_alunos INTEGER,
                    instrutor INTEGER,
                    horainicio VARCHAR(255),
                    horafinal VARCHAR(255)
                );   
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Inscricoes(
                  id_aula INTEGER PRIMARY KEY,
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
    def CriarAulaDeGrupo(self, instrutor : Utilizador, horainicio, horafinal, limit):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                INSERT INTO Aulasgrupo (instrutor, horainicio, horafinal, limite_alunos) VALUES (?,?,?,?)            
            ''', (instrutor.id, horainicio, horafinal, limit))
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
                alunos.append(Utilizador(aluno[1], aluno[0], aluno[2], aluno[3], aluno[4], aluno[5]))
            return alunos
        except sqlite3.Error as error:
            print('Ocorreu um erro ao listar alunos', error)
    def ListarInstrutores(self) -> list[Instrutor]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("""SELECT * FROM Instrutores""")
            self.sqliteConnection.commit()
            raw_instrutores = cursor.fetchall()
            
            instrutores = []
            for instrutor in raw_instrutores:
                instrutores.append(Instrutor(instrutor[1], instrutor[0], instrutor[2], instrutor[3], instrutor[4], instrutor[5]))
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
                #TODO: adicionar id á aula de grupo 
                aulas.append(Aulasgrupo(self.ProcurarInstrutorID(aula[2]),datetime.datetime.strptime(aula[3], "%d/%m/%Y %H:%M"), datetime.datetime.strptime(aula[4], "%d/%m/%Y %H:%M"), aula[1]))
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
    def ListarInscricoesDeAula(self, alta : Aulasgrupo) -> list[Utilizador]:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute("SELECT * FROM Inscricoes WHERE id_aula = ?", (1,)) #TODO: mudar 1 pela id da aula
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
            return Utilizador(raw_instrutor[1], raw_instrutor[0], raw_instrutor[2], raw_instrutor[3], raw_instrutor[4], raw_instrutor[5])
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)
    def ProcurarInstrutorID(self, id) -> Utilizador:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('SELECT * FROM Instrutores WHERE id = ?', (id,))
            raw_instrutor = cursor.fetchone()
            if(raw_instrutor == None):
                return None
            return Instrutor(raw_instrutor[1], raw_instrutor[0], raw_instrutor[2], raw_instrutor[3], raw_instrutor[4], raw_instrutor[5])
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)
    def ProcurarAulaID(self, id) -> Aulasgrupo:
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('SELECT * FROM Aulasgrupo WHERE id = ?', (id,))
            raw_aula = cursor.fetchone()
            if(raw_aula == None):
                return None
            #TODO: adicionar id á aula de grupo
            return Aulasgrupo(self.ProcurarInstrutorID(raw_aula[2]),datetime.datetime.strptime(raw_aula[3], "%d/%m/%Y %H:%M"), datetime.datetime.strptime(raw_aula[4], "%d/%m/%Y %H:%M"), raw_aula[1])
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)