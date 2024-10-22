import curses
import sys
from time import sleep
from .logica import Logica, Utilizador, Aulasgrupo, Instrutor
import io
TAB_WINDOW = "TAB"
CONTENT_WINDOW = "CONTENT"

class Tabs:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.window = curses.newwin(3, self.stdscr.getmaxyx()[1], 0, 0)
        self.tabs = ["Página inicial","Alunos", "Instrutores", "Aulas de Grupo"]
        self.selected = 0
    def separators(self, max_columns, columns_per_each, leftover_columns):
       self.window.hline(0,0,'-', max_columns)
       self.window.hline(2,0,'-', max_columns)
       
       self.window.addch(0,0, "+")
       self.window.addch(0,max_columns, "+")
       self.window.addch(2,0, "+")
       self.window.addch(2,max_columns, "+")
       for i in range(1, len(self.tabs)):
           self.window.addch(0,columns_per_each*i+leftover_columns,"+")
           self.window.addch(1,columns_per_each*i+leftover_columns,"|")
           self.window.addch(2,columns_per_each*i+leftover_columns,"+")

       self.window.addch(1,0,'|')
       self.window.addch(1,max_columns,'|')
    def header(self):
        max_columns = self.stdscr.getmaxyx()[1] - 2
        columns_per_each = max_columns // len(self.tabs)
        leftover_columns = max_columns  % len(self.tabs)
        self.window.move(0,0)
        self.separators(max_columns, columns_per_each,leftover_columns)
        ###
        self.window.move(1, 1)
        for i in range(len(self.tabs)):
            start = columns_per_each*i+leftover_columns
            size = columns_per_each - 2
            tab = self.tabs[i]
            if i == 0:
                size += leftover_columns
                start = 0
            
            attr = 0
            if self.selected == i:
                attr = curses.A_BOLD

            if len(tab) < size: 
                self.window.addstr(1,((size - len(tab))// 2) + start+1,tab,attr)
            elif len(tab) == size:
                self.window.addstr(1,start,tab,attr)
            else:
                tab = tab[0:size-2] + "..."
                self.window.addstr(1,start+1, str(tab))
                pass
        ###
    def clear(self):
        self.window.erase()
    def refresh(self):
        self.window.refresh()
    def render(self):
        self.header()
    def resize(self, lines, cols):
        self.window.resize(3, cols)
        self.window.refresh()
class Content:
    def pagina_inicial(self):
        page = self.pages[0]
        page.addstr("Gym Manager\n", curses.A_BOLD)
        page.addstr("Feito por ")
        page.addstr("Rodrigo Vieira", curses.A_BOLD)
        page.addstr(", ")
        page.addstr("Diogo Costa", curses.A_BOLD)
        page.addstr(", ")
        page.addstr("Afonso Batista", curses.A_BOLD)
        page.addstr(" no ambito da UFCD 10793\n\n")
        page.addstr("Como utilizar?\n", curses.A_BOLD)
    def pagina_alunos(self):
        def var_maior(alunos, attr):
            maior = 0
            for i in alunos:
                maior = max(maior, len(str(getattr(i, attr))))
            return maior

        titulos = ["Nome", "ID", "Telefone", "Email", "Morada", "Idade"]
        attrs = ["nome", "id", "telefone", "email", "morada", "idade"]
        alinhamentos = [c for attr in attrs if(c := var_maior(self.alunos, attr))]
        for i in range(len(alinhamentos)):
            alinhamentos[i] = max(alinhamentos[i], len(titulos[i]))

        print(alinhamentos)
        page = self.pages[1]
        page.erase()
        page.resize(255, sum(alinhamentos) + len(titulos)*3 + 1)

        #px = 86
        #[14, 2, 9, 23, 14, 5]
        py,px = page.getmaxyx()
        print(px)
        colunas_por_titl = px // len(titulos)
        resto_colunas =  px % len(titulos)
        
        page.move(2,1)
        page.hline("-", px-1)
        page.move(1,0)
        page.vline("|", 255)
        offset:int = 0
        for i in alinhamentos:
            offset += i + 3
            page.vline(1, offset, "|", 255)
        offset = 1
        for i in range(len(titulos)):
            titulo = titulos[i]
            alinhamento = alinhamentos[i] + 2
            size = (alinhamento - len(titulo))//2
            page.addstr(1, offset + size, titulo)  
            offset += alinhamentos[i] + 3

        linha = 3
        for aluno in self.alunos:
            offset = 2
            for i in range(len(attrs)):
                attr = attrs[i]
                #page.addch(linha, offset, "/")
                page.addstr(linha, offset, str(getattr(aluno, attr)))
                offset += alinhamentos[i] + 3
            linha+=1
            print(linha, offset)

        return
        for i in range(len(titulos)): 
            alinhamento = alinhamentos[i]
            titulo = titulos[i]
            size = alinhamento - len(titulo)
            print(alinhamento,len(titulo), size)
            offset = 0
            for x in range(i):
                offset += alinhamentos[x]
            page.move(1, offset + size//2)
            page.addstr(titulos[i])
            #for x in range(alinhamento):
            #    page.addch("-")
            #page.addch("|")
        #for i in range(len(titulos)):
        #    titulo = titulos[i]
        #    size = colunas_por_titl
        #    if i == 0:
        #        size += resto_colunas

        #    page.addstr(f"{titulo} ")
        #print(attrs)

        

    def __init__(self, tui, stdscr):
        self.stdscr = stdscr
        self.tui = tui
        y, x = self.stdscr.getmaxyx()
        self.window = curses.newwin(y-3, x, 3, 0)
        self.pages = [
            curses.newpad(10, 255),
            curses.newpad(1, 1)
        ]
        self.alunos = [
            Utilizador("Rodrigo Vieira", 0, "938663683", "rodrigovieira@gmail.com", "Rua das Ruas 1", 16),
            Utilizador("Diogo Costa",    1, "938663683", "diogocosta@gmail.com",    "Rua das Ruas 2", 16),
            Utilizador("Afonso Batista", 2, "938663683", "rodrigovieira@gmail.com", "Rua das Ruas 3", 16)
        ]

        self.pagina_inicial()
        self.pagina_alunos()


    def clear(self):
        self.window.erase()
    def refresh(self):
        #self.window.refresh()
        pass
    def resize(self, lines, cols):
        self.window.resize(lines - 3, cols)
        self.window.refresh()
    
        
    def render(self):
        #self.window.refresh()
        selected = self.tui.selected
        wy,wx = self.window.getmaxyx()
        wx -= 1
        wx -= 1
        if(selected < len(self.pages)):
            page = self.pages[selected]
            py,px = self.pages[selected].getmaxyx()
            y = min(wy, py)
            x = min(wx, px)
            #print(f"wx:{wx} wy: {wy} px:{px} py:{py} x:{x} y:{y}")
            page.refresh(0,0,3,0,y, x)
        
        self.window.move(wy-1, 0)
        #Desenhar o scroll horizontal com o caracter bloco (alt + 219)
        #for i in range(wx):
            #self.window.addch("█")
        #Scroll vertical
        #for i in range(wy):
            #self.window.addch(i, wx-1, "█")


class Tui:
    def __clear(self):
        for (_, w) in self.windows.items():
            w.clear()
    def __refresh(self):
        for (_, w) in self.windows.items():
            w.refresh()
    def __resize(self, lines, cols):
        curses.resize_term(lines, cols)
        self.stdscr.resize(lines, cols)
        self.stdscr.erase()
        for (_, w) in self.windows.items():
            w.resize(lines, cols)
            w.clear()

    def __render(self):
        for (_, w) in self.windows.items():
            w.render()
            w.refresh()
    def __setup(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(1)
        self.lines, self.cols = self.stdscr.getmaxyx()
        self.windows = {}
        self.windows[TAB_WINDOW] = Tabs(self.stdscr)
        self.windows[CONTENT_WINDOW] = Content(self.windows[TAB_WINDOW], self.stdscr)

        curses.curs_set(0)
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_RESIZE:
                self.stdscr.erase()
                y, x = self.stdscr.getmaxyx()
                print(f"Resize from ({self.lines}, {self.cols}) to ({y},{x})")
                self.lines, self.cols = y, x
                self.__resize(y, x)
            self.__clear()
            self.__render()
            self.__refresh()
            print(ch)
            if ch == curses.KEY_LEFT:
                self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected - 1) % len(self.windows[TAB_WINDOW].tabs)
                self.stdscr.erase()
            elif ch == curses.KEY_RIGHT:
                self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected + 1) % len(self.windows[TAB_WINDOW].tabs)
                self.stdscr.erase()
            sleep(0.1)
    def run(self):
        f = open("log.txt", "w")
        sys.stdout = f
        curses.wrapper(self.__setup)
       