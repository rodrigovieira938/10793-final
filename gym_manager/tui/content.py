import curses
from ._tui import Tui, TAB_WINDOW, VERTICAL_SCROLLBAR, HORIZONTAL_SCROLLBAR
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
        self.pad = curses.newpad(255, 255) # -3 para o header -1 para a scrollbar
        self.selected = 0
        self.pages = [
            PagInicial(self),
            PagRegistrar(self),
            PagAlunos(self),
            PagInstrutor(self),
            PagAulas(self),
        ]

    def resize(self):
        pass #Não é preciso já que usa um pad e não uma window
    def render(self):
        self.pad.clear()
        self.pages[self.selected].render()
        self.pad.refresh(0,0,3,0, self.tui.maxlines-4, self.tui.maxcols-3)
    def preswitch(self, selected):
        self.pages[selected].preswitch()
    def switch(self, selected):
        self.selected = selected
        self.pages[selected].switch()
