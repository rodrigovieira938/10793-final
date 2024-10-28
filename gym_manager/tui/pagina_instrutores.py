from .content import Content, curses, PAGINA_INSTRUTOR
from .scrollbar import Scrollbar
from ._tui import TAB_WINDOW
class PagInstrutores:
    def __init__(self, content : Content):
        self.content = content
        self.instrutores = []
        self.vscrollbar = Scrollbar(self.content.tui, True)
        self.hscrollbar = Scrollbar(self.content.tui, False)
        self.state = 0
    def preswitch(self):
        pass
    def switch(self):
        self.content.tui.screen.erase()
        self.instrutores = self.content.tui.logica.db.ListarInstrutores()
        self.vscrollbar.needed = True
        self.vscrollbar.max = len(self.instrutores)

        self.hscrollbar.resize()
        self.vscrollbar.resize()
    def resize(self):
        self.vscrollbar.resize()
        self.hscrollbar.resize()
    def input(self, ch):
        if ch == curses.KEY_DOWN and self.vscrollbar.max > 0:
            self.vscrollbar.current = (self.vscrollbar.current + 1) % self.vscrollbar.max
        elif ch == curses.KEY_UP and self.vscrollbar.max > 0:
            self.vscrollbar.current = (self.vscrollbar.current - 1) % self.vscrollbar.max
        elif ch == curses.KEY_RIGHT and self.hscrollbar.needed and (self.hscrollbar.current+1) <= self.hscrollbar.max      and self.hscrollbar.max > 0:
            self.hscrollbar.current = (self.hscrollbar.current + 1)
        elif ch == curses.KEY_LEFT and self.hscrollbar.needed  and 0 <= (self.hscrollbar.current-1) <= self.hscrollbar.max and self.hscrollbar.max > 0:
            self.hscrollbar.current = (self.hscrollbar.current - 1)
        elif ch == ord("\n"):
            if len(self.instrutores) == 0:
                return
            self.content.pages[PAGINA_INSTRUTOR].instrutor = self.instrutores[self.vscrollbar.current]
            self.content.preswitch(PAGINA_INSTRUTOR)
            self.content.tui.windows[TAB_WINDOW].selected_before = self.content.tui.windows[TAB_WINDOW].selected
            self.content.tui.windows[TAB_WINDOW].selected = PAGINA_INSTRUTOR
            self.content.switch(PAGINA_INSTRUTOR)
    def render(self):
        page = self.content.pad
        selected_color = self.content.tui.selected_color

        def var_maior(alunos, attr):
            maior = 0
            for i in alunos:
                maior = max(maior, len(str(getattr(i, attr))) +2)
            return maior
        attrs = [("Nome","nome"), ("ID", "id"), ("Telefone", "telefone"), ("Email","email"), ("Morada", "morada"), ("Idade","idade")]
        alinhamentos = [c for attr in attrs if(c := var_maior(self.instrutores, attr[1]))]
        if len(alinhamentos) > 0:
            for i in range(len(attrs)):
                if len(alinhamentos) == 0:
                    alinhamentos.append(len(attrs[i][0])+2)
                else:
                    alinhamentos[i] = max(alinhamentos[i], len(attrs[i][0])+2)
        else:
            alinhamentos = [len(titulo)+2 for (titulo,_) in attrs]
        page.erase()
        cols_needed = sum(alinhamentos) + len(attrs) + 1
        page.resize(255, cols_needed)
        
        page.hline(2,1,"-", cols_needed-2)
        page.vline(1,0,"|", 255)

        offset:int = 0
        for i in alinhamentos:
            offset += i + 1
            page.vline(1, offset, "|", 255)

        if len(self.instrutores) > 0:
            if curses.has_colors():
                page.addch(3,0, " ", selected_color)
                page.addch(3,cols_needed-1, " ", selected_color)
            else:
                page.addch(3,0, "X")
                page.addch(3,cols_needed-1, "X")
        

        offset = 1
        for i in range(len(alinhamentos)):
            titulo = attrs[i][0]
            alinhamento = alinhamentos[i]
            size = (alinhamento - len(titulo))//2
            page.addstr(1, offset+size, titulo)  
            offset += alinhamentos[i] + 1
       
        line = 3
        start = self.vscrollbar.current
        for x in range(start, len(self.instrutores)):
            aluno = self.instrutores[x]
            offset = 2
            color = 0
            if self.vscrollbar.current == x and curses.has_colors():
                color = selected_color
                for i in range(1, cols_needed-1):
                    page.addch(line, i, " ", color)
                
            for i in range(len(attrs)):
                attr = attrs[i]
                page.addstr(line, offset, str(getattr(aluno, attr[1])), color)
                offset += alinhamentos[i] + 1
            line+=1
            if line >= 255:
                break
        if cols_needed > self.content.tui.maxcols - 2: # -2 para o limite e para a scrollbar
            self.hscrollbar.needed = True
            self.hscrollbar.max = cols_needed - (self.content.tui.maxcols - 2)# +2 para o limite e para a scrollbar
        else:
            self.hscrollbar.current = 0
        self.vscrollbar.render()
        self.hscrollbar.render()
    def refresh(self):
        offset = self.hscrollbar.current
        self.content.pad.refresh(0,offset,3,0, self.content.tui.maxlines-1-2, self.content.tui.maxcols-1-2) # -2 para o espaço em branco entre a scrollbar e o tamanho da scrollbar e -1 para o limite
        self.vscrollbar.refresh()
        self.hscrollbar.refresh()