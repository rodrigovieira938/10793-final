import curses
from ._tui import Tui, TAB_WINDOW, VERTICAL_SCROLLBAR, HORIZONTAL_SCROLLBAR
from ..logica import Utilizador

class Content:
    def __init__(self, tui: Tui):
        self.tui = tui
        self.maxcols = tui.maxcols
        self.maxlines = tui.maxlines
        self.pad = curses.newpad(255, 255) # -3 para o header -1 para a scrollbar
        self.alunos = [
        ]
        for i in range(255):
            user = Utilizador("Rodrigo Vieira", 0, "938663683", "rodrigovieira@gmail.com", "Rua das Ruas 1", 16)
            user.id = i
            user.idade = i
            self.alunos.append(user)
    def resize(self):
        pass #Não é preciso já que usa um pad e não uma window
    def pagina_inicial(self):
        self.pad.addstr("Gym Manager\n", curses.A_BOLD)
        self.pad.addstr("Feito por ")
        self.pad.addstr("Rodrigo Vieira", curses.A_BOLD)
        self.pad.addstr(", ")
        self.pad.addstr("Diogo Costa", curses.A_BOLD)
        self.pad.addstr(", ")
        self.pad.addstr("Afonso Batista", curses.A_BOLD)
        self.pad.addstr(" no ambito da UFCD 10793\n\n")
        self.pad.addstr("Como utilizar?\n", curses.A_BOLD)
    def pagina_alunos(self):
        vscrollbar = self.tui.windows[VERTICAL_SCROLLBAR] 
        if len(self.alunos)+3 > 255:
            vscrollbar.needed = True
            vscrollbar.max = len(self.alunos)

        page = self.pad

        def var_maior(alunos, attr):
            maior = 0
            for i in alunos:
                maior = max(maior, len(str(getattr(i, attr))))
            return maior

        attrs = [("Nome","nome"), ("ID", "id"), ("Telefone", "telefone"), ("Email","email"), ("Morada", "morada"), ("Idade","idade")]
        alinhamentos = [c for attr in attrs if(c := var_maior(self.alunos, attr[1]))]
        for i in range(len(attrs)):
            alinhamentos[i] = max(alinhamentos[i], len(attrs[i][0]))

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
    def render(self):
        self.pad.clear()
        match self.tui.windows[TAB_WINDOW].selected:
            case 0:
                self.pagina_inicial()
            case 1:
                self.pagina_alunos()
            case 2:
                self.pad.addstr("Terceira tab")
            case 3:
                self.pad.addstr("Quarta tab")
            case _: pass
        self.pad.refresh(0,0,3,0, self.tui.maxlines-4, self.tui.maxcols-3)
