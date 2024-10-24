import curses
from ._tui import Tui

class Header:
    def __init__(self, tui: Tui):
        self.tabs = ["Página inicial","Registrar" ,"Alunos", "Instrutores", "Aulas de Grupo"]
        self.selected = 0
        self.tui = tui
        self.maxcols = tui.maxcols
        self.maxlines = tui.maxlines
        self.window = curses.newwin(3, tui.maxcols)
    def resize(self):
        self.maxcols = self.tui.maxcols
        self.maxlines = self.tui.maxlines
        self.window.resize(3, self.maxcols)
    def render(self):
        self.window.erase()
        
        max_columns = self.maxcols - 2 # - 1 para o limite e -1 para a primeira coluna
        columns_per_each = max_columns // len(self.tabs)
        leftover_columns = max_columns  % len(self.tabs)

        self.window.addch(1,0, "|")
        self.window.addch(1,self.maxcols-2, '|')
        self.window.hline(0,1, "-", self.maxcols-2)
        self.window.hline(2,1, "-", self.maxcols-2)

        self.window.addch(0,0, "+")
        self.window.addch(2,0, "+")
        self.window.addch(0,self.maxcols-2, "+")
        self.window.addch(2,self.maxcols-2, "+")

        for i in range(1, len(self.tabs)):
            self.window.addch(0,columns_per_each*i+leftover_columns,"+")
            self.window.addch(1,columns_per_each*i+leftover_columns,"|")
            self.window.addch(2,columns_per_each*i+leftover_columns,"+")
        
        self.window.move(1, 1)
        for i in range(len(self.tabs)):
            start = columns_per_each*i+leftover_columns+1
            size = columns_per_each - 1
            tab = self.tabs[i]
            if i == 0:
                size += leftover_columns
                start = 1
            
            attr = 0
            if self.selected == i:
                attr = curses.A_BOLD

            if len(tab) < size: 
                center = ((size - len(tab)) // 2) + ((size - len(tab)) % 2)
                self.window.addstr(1,center + start,tab,attr)
            elif len(tab) == size:
                self.window.addstr(1,start,tab,attr)
            else:
                tab = tab[0:size-3] + "..."
                center = ((size - len(tab)) // 2) + ((size - len(tab)) % 2)
                self.window.addstr(1,start+center, str(tab))
                pass

        self.window.refresh()
