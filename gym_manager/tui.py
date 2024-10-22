import curses
import sys
from time import sleep

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
        print(f"Rendering header with width: {max_columns}")
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

                print(len(tab), tab)
                self.window.addstr(1,start+1, str(tab))
                pass
        ###
    def clear(self):
        self.window.clear()
    def refresh(self):
        self.window.refresh()
    def render(self):
        self.header()
    def resize(self, lines, cols):
        print("Resize Tabs")
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
    

    def __init__(self, tui, stdscr):
        self.stdscr = stdscr
        self.tui = tui
        y, x = self.stdscr.getmaxyx()
        self.window = curses.newwin(y-3, x, 3, 0)
        self.pages = [
            curses.newpad(10, 255)
        ]
        self.pagina_inicial()
    def clear(self):
        self.window.clear()
        pass
    def refresh(self):
        self.window.refresh()
        if(self.tui.selected < len(self.pages)):
            page = self.pages[0]
            wy,wx = self.window.getmaxyx()
            wy -= 3
            wx -= 1
            py,px = self.pages[0].getmaxyx()
            y = min(wy, py)
            x = min(wx, px)
            page.refresh(
                0,0,
                3,1,
                y, x)
    def resize(self, lines, cols):
        self.window.resize(lines - 3, cols)
        self.window.refresh()
    
        
    def render(self):
        #self.pagina_inicial()
        pass


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
        self.stdscr.clear()
        for (_, w) in self.windows.items():
            w.resize(lines, cols)
            w.clear()

    def __render(self):
        for (_, w) in self.windows.items():
            w.render()
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
                self.stdscr.clear()
                y, x = self.stdscr.getmaxyx()
                print(f"Resize from ({self.lines}, {self.cols}) to ({y},{x})")
                self.lines, self.cols = y, x
                self.__resize(y, x)
            elif ch == curses.KEY_LEFT:
                self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected - 1) % len(self.windows[TAB_WINDOW].tabs)
            elif ch == curses.KEY_RIGHT:
                self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected + 1) % len(self.windows[TAB_WINDOW].tabs)
            self.__clear()
            self.__render()
            self.__refresh()
            sleep(0.1)
    def run(self):
        f = open("log.txt", "w")
        sys.stdout = f
        curses.wrapper(self.__setup)
       