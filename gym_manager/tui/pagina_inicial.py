from .content import Content, curses

class PagInicial:
    def __init__(self, content : Content):
        self.content = content
    def preswitch(self):
        pass
    def switch(self):
        self.content.tui.screen.erase()
        self.resize()
    def resize(self):
        self.content.pad.resize(self.content.maxlines, self.content.maxcols)
    def input(self, ch):
        pass
    def render(self):
        self.content.pad.addstr("Este trabalho foi solicitado pelo formador Gonçalo Feliciano na UFCD 10793. Neste trabalho temos um gymmanger com alunos instrutores e aulas de grupo.", curses.A_BOLD)
    def refresh(self):
        self.content.pad.refresh(0,0,3,0, self.content.maxlines-1, self.content.maxcols-1)