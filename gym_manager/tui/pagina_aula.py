from .content import Content, curses
from .scrollbar import Scrollbar

class PagAula:
    def __init__(self, content : Content):
        self.content = content
        self.aula = None
        self.alunos = None
        self.vscrollbar = Scrollbar(self.content.tui, True)
        self.hscrollbar = Scrollbar(self.content.tui, False)
    def preswitch(self):
        pass
    def switch(self):
        self.content.tui.screen.erase()
        self.alunos = self.content.tui.logica.db.ListarInscricoesDeAula(self.aula)
        self.vscrollbar.needed = True
        self.vscrollbar.max = len(self.alunos)
    def resize(self):
        self.vscrollbar.resize()
        self.hscrollbar.resize()
    def input(self, ch):
        if ch == curses.KEY_DOWN and self.vscrollbar.max > 0:
            self.vscrollbar.current = (self.vscrollbar.current + 1) % self.vscrollbar.max
        elif ch == curses.KEY_UP and self.vscrollbar.max > 0:
            self.vscrollbar.current = (self.vscrollbar.current - 1) % self.vscrollbar.max
        elif ch == curses.KEY_RIGHT and self.hscrollbar.needed and (self.hscrollbar.current+1) <= self.hscrollbar.max:
            self.hscrollbar.current = (self.hscrollbar.current + 1)
        elif ch == curses.KEY_LEFT and self.hscrollbar.needed  and 0 <= (self.hscrollbar.current-1) <= self.hscrollbar.max:
            self.hscrollbar.current = (self.hscrollbar.current - 1)
    def render(self):
        page = self.content.pad
        page.erase()
        txt = f"Alunos incritos na aula \"{self.aula.nome}\" ({self.aula.id}) com {self.aula.instrutor.nome} ({self.aula.instrutor.id})\n"
        page.addstr(txt)

        ### Igual a Pagina Alunos
        def var_maior(alunos, attr):
            maior = 0
            for i in alunos:
                maior = max(maior, len(str(getattr(i, attr))) +2)
            return maior
        attrs = [("Nome","nome"), ("ID", "id"), ("Telefone", "telefone"), ("Email","email"), ("Morada", "morada"), ("Idade","idade")]
        alinhamentos = [c for attr in attrs if(c := var_maior(self.alunos, attr[1]))]
        if len(alinhamentos) > 0:
            for i in range(len(attrs)):
                if len(alinhamentos) == 0:
                    alinhamentos.append(len(attrs[i][0])+2)
                else:
                    alinhamentos[i] = max(alinhamentos[i], len(attrs[i][0])+2)
        else:
            alinhamentos = [len(titulo)+2 for (titulo,_) in attrs]
        cols_needed = sum(alinhamentos) + len(attrs) + 1
        page.resize(255, max(cols_needed, len(txt)))
        
        page.hline(3,1,"-", cols_needed-2)
        page.vline(2,0,"|", 255)

        offset:int = 0
        for i in alinhamentos:
            offset += i + 1
            page.vline(2, offset, "|", 255)
        offset = 1
        for i in range(len(alinhamentos)):
            titulo = attrs[i][0]
            alinhamento = alinhamentos[i]
            size = (alinhamento - len(titulo))//2
            page.addstr(2, offset+size, titulo)  
            offset += alinhamentos[i] + 1
        
        line = 4
        start = self.vscrollbar.current
        for x in range(start, len(self.alunos)):
            aluno = self.alunos[x]
            offset = 2
            for i in range(len(attrs)):
                attr = attrs[i]
                page.addstr(line, offset, str(getattr(aluno, attr[1])))
                offset += alinhamentos[i] + 1
            line+=1
            if line >= 255:
                break
        if max(cols_needed,len(txt)) > self.content.tui.maxcols - 2: # -2 para o limite e para a scrollbar
            self.hscrollbar.needed = True
            self.hscrollbar.max = max(cols_needed,len(txt)) - (self.content.tui.maxcols - 2)# +2 para o limite e para a scrollbar
        else:
            self.hscrollbar.current = 0
        self.vscrollbar.render()
        self.hscrollbar.render()
    def refresh(self):
        offset = self.hscrollbar.current
        self.content.pad.refresh(0,offset,3,0, self.content.tui.maxlines-1-2, self.content.tui.maxcols-1-2) # -2 para o espaço em branco entre a scrollbar e o tamanho da scrollbar e -1 para o limite
        self.vscrollbar.refresh()
        self.hscrollbar.refresh()