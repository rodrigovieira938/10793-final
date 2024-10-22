import sqlite3

class Db:
    def __init__(self):
        try:
            self.sqliteConnection = sqlite3.connect('dados.db')
            
        except sqlite3.Error as error:
            print('Ocorreu um erro', error) 
            
    def tabela(self):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Utilizadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                    telefone INT
                    email VARCHAR(255) NOT NULL
                    morada TEXT NOT NULL
                    idade INT
                    aulas TEXT NOT NULL
            );
                CREATE TABLE IF NOT EXISTS Instrutor(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                    telefone INT
                    email VARCHAR(255) NOT NULL
                    morada TEXT NOT NULL
                    idade INT
                    aulas TEXT NOT NULL 
            );
                CREATE TABLE IF NOT EXISTS Aulasgrupo(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    instrutor TEXT NOT NULL
                    horainicio TIMESTAMP
                    horafinal TIMESTAMP
                    limit INT
                    alunos TEXT NOT NULL
            );                                                  
        ''')
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro', error)
              
    def CriarUtilizador(self, nome, telefone, email, morada, idade, aulas):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                INSERT INTO Utilizadores (nome, telefone, email, morada, idade, aulas)
            ''', (nome, telefone, email, morada, idade, aulas))
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro ao criar utilizador', error)
        
        
    def CriarInstrutor(self, nome, telefone, email, morada, idade, aulas):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                INSERT INTO Instrutor (nome, telefone, email, morada, idade, aulas)               
            ''', (nome, telefone, email, morada, idade, aulas))
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro ao criar o Instrutor', error)
            
            
    def CriarAulaDeGrupo(self, instrutor, horainicio, horafinal, limit, alunos):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('''
                INSERT INTO Utilizadores (instrutor, horainicio, horafinal, limit, alunos)               
            ''', (instrutor, horainicio, horafinal, limit, alunos))
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro ao criar as Aulas', error)
            
            
    def AdicionarUtilizadorAAula(self,utilizador, aula):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('INSERT INTO Inscricoes (aluno_id, aula_id) VALUES (?, ?)', (utilizador, aula))
            self.sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Ocorreu um erro ao adicionar utilizador à aula', error)
        
        
    def ProcurarUtilizadorID(self, id):
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute('SELECT * FROM Utilizadores WHERE id = ?', (id,))
            
            for linha in cursor:
                print(linha) 
                return linha 
            print("Nenhum resultado encontrado.") 
        except sqlite3.Error as error:
            print('Ocorreu um erro ao procurar utilizador', error)
