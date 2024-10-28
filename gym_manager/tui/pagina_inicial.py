from .content import Content, curses

class PagInicial:
    def __init__(self, content : Content):
        self.content = content
        self.maxlines = 0
        self.maxcols = 0
        self.resize()
    def preswitch(self):
        pass
    def switch(self):
        self.content.tui.screen.erase()
        self.resize()
    def resize(self):
        self.maxlines = self.content.tui.maxlines
        self.maxcols = self.content.tui.maxcols
        self.content.pad.resize(self.maxlines, self.maxcols)
    def input(self, ch):
        pass
    def render(self):
        self.content.pad.addstr("Este trabalho foi solicitado pelo formador Gonçalo Feliciano na UFCD 10793.\nNeste trabalho temos um gymmanger com alunos instrutores e aulas de grupo.", curses.A_BOLD)
    def refresh(self):
        self.content.pad.refresh(0,0,3,0, self.maxlines-1, self.maxcols-1)