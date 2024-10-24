from .content import Content, curses
from ._tui import VERTICAL_SCROLLBAR
from curses.textpad import Textbox

class PagAlunos:
    def __init__(self, content : Content):
        self.content = content
        self.alunos = []
    def preswitch(self):
        pass
    def switch(self):
        self.content.tui.logica.CriarUtilizador("Rodrigo Ribeiro", "telefone", "email", "morada", "idade")
        self.alunos = self.content.tui.logica.db.ListarAlunos()
    def render(self):
        vscrollbar = self.content.tui.windows[VERTICAL_SCROLLBAR] 
        if len(self.alunos)+3 > 255:
            vscrollbar.needed = True
            vscrollbar.max = len(self.alunos)

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

        py,px = page.getmaxyx()
        colunas_por_titl = px // len(alinhamentos)
        resto_colunas =  px % len(alinhamentos)
        
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
        start = vscrollbar.current
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