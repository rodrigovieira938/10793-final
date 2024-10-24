from .content import Content, curses

class PagInicial:
    def __init__(self, content : Content):
        self.content = content
    def preswitch(self):
        pass
    def switch(self):
        pass
    def render(self):
        self.content.pad.addstr("Gym Manager\n", curses.A_BOLD)
        self.content.pad.addstr("Feito por ")
        self.content.pad.addstr("Rodrigo Vieira", curses.A_BOLD)
        self.content.pad.addstr(", ")
        self.content.pad.addstr("Diogo Costa", curses.A_BOLD)
        self.content.pad.addstr(", ")
        self.content.pad.addstr("Afonso Batista", curses.A_BOLD)
        self.content.pad.addstr(" no ambito da UFCD 10793\n\n")
        self.content.pad.addstr("Como utilizar?\n", curses.A_BOLD)