from .content import Content, curses
from curses.textpad import Textbox
from .scrollbar import Scrollbar

class PagAlunos:
    def __init__(self, content : Content):
        self.content = content
        self.alunos = []
        self.vscrollbar = Scrollbar(self.content.tui, True)
        self.hscrollbar = Scrollbar(self.content.tui, False)
    def preswitch(self):
        pass
    def resize(self):
        self.vscrollbar.resize()
        self.hscrollbar.resize()
    def switch(self):
        self.alunos = self.content.tui.logica.db.ListarAlunos()
    def input(self, ch):
        if ch == curses.KEY_DOWN and self.vscrollbar.needed:
            self.vscrollbar.current = (self.vscrollbar.current + 1) % self.vscrollbar.max
        elif ch == curses.KEY_UP and self.vscrollbar.needed:
            self.vscrollbar.current = (self.vscrollbar.current - 1) % self.vscrollbar.max
        elif ch == curses.KEY_RIGHT and self.hscrollbar.needed:
            self.hscrollbar.current = (self.hscrollbar.current + 1) % self.hscrollbar.max
        elif ch == curses.KEY_LEFT and self.hscrollbar.needed:
            self.hscrollbar.current = (self.hscrollbar.current - 1) % self.hscrollbar.max
    def render(self):
        if len(self.alunos)+3 > 255:
            self.vscrollbar.needed = True
            self.vscrollbar.max = len(self.alunos)

        page = self.content.pad

        def var_maior(alunos, attr):
            maior = 0
            for i in alunos:
                maior = max(maior, len(str(getattr(i, attr))))
            return maior

        attrs = [("Nome","nome"), ("ID", "id"), ("Telefone", "telefone"), ("Email","email"), ("Morada", "morada"), ("Idade","idade")]
        alinhamentos = [c for attr in attrs if(c := var_maior(self.alunos, attr[1]))]
        if len(alinhamentos) > 0:
            for i in range(len(attrs)):
                if len(alinhamentos) == 0:
                    alinhamentos.append(len(attrs[i][0]))
                else:
                    alinhamentos[i] = max(alinhamentos[i], len(attrs[i][0]))
        else:
            alinhamentos = [len(titulo) for (titulo,_) in attrs]
        page.erase()
        cols_neeeded = sum(alinhamentos) + len(attrs)*3 + 1
        page.resize(255, cols_neeeded)

        if cols_neeeded > self.content.maxcols:
            self.hscrollbar.needed = True
            self.hscrollbar.max = cols_neeeded-self.content.maxcols
            print(self.hscrollbar.max)

        _,px = page.getmaxyx()
        
        page.move(2,1)
        page.hline("-", px-1)
        page.move(1,0)
        page.vline("|", 255)
        offset:int = 0
        for i in alinhamentos:
            offset += i + 3
            page.vline(1, offset, "|", 255)
        offset = 1
        for i in range(len(alinhamentos)):
            titulo = attrs[i][0]
            alinhamento = alinhamentos[i] + 2
            size = (alinhamento - len(titulo))//2
            page.addstr(1, offset + size, titulo)  
            offset += alinhamentos[i] + 3
        line = 3
        start = self.vscrollbar.current
        for x in range(start, len(self.alunos)):
            aluno = self.alunos[x]
            offset = 2
            for i in range(len(attrs)):
                attr = attrs[i]
                page.addstr(line, offset, str(getattr(aluno, attr[1])))
                offset += alinhamentos[i] + 3
            line+=1
            if line >= 255:
                break
    def refresh(self):
        self.content.pad.refresh(0,self.hscrollbar.current,3,0, self.content.tui.maxlines-1-2, self.content.tui.maxcols-2) # -2 para o espaço em branco entre a scrollbar e o tamanho da scrollbar 
        self.vscrollbar.render()
        self.hscrollbar.render()