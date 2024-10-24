import curses
from ._tui import Tui, TAB_WINDOW
from ..logica import Utilizador

class Content:
    def __init__(self, tui: Tui):
        from .pagina_inicial import PagInicial
        from .pagina_registrar import PagRegistrar
        from .pagina_alunos import PagAlunos
        from .pagina_instrutores import PagInstrutor
        from .pagina_aulas import PagAulas

        self.tui = tui
        self.maxcols = tui.maxcols
        self.maxlines = tui.maxlines
        self.pad = curses.newpad(255, 255)
        self.selected = 0
        self.pages = [
            PagInicial(self),
            PagRegistrar(self),
            PagAlunos(self),
            PagInstrutor(self),
            PagAulas(self),
        ]
    def resize(self):
        self.maxcols = self.tui.maxcols
        self.maxlines = self.tui.maxlines
        self.pages[self.selected].resize()
    def render(self):
        self.pad.clear()
        self.pages[self.selected].render()
        self.pages[self.selected].refresh()
    def input(self, ch):
        self.pages[self.selected].input(ch)
    def preswitch(self, selected):
        self.pages[selected].preswitch()
    def switch(self, selected):
        self.selected = selected
        self.pages[selected].switch()
