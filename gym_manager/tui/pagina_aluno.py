from .content import Content, curses
from .scrollbar import Scrollbar
import datetime

class PagAluno:
    def __init__(self, content : Content):
        self.content = content
        self.aluno = None
        self.aulas = []
        self.aulas_inscrever = []
        self.vscrollbar = Scrollbar(self.content.tui, True)
        self.hscrollbar = Scrollbar(self.content.tui, False)
        self.state = 0
        self.selected = 0
        self.buttons = ["Adicionar Aluno a Aula", "Ver aulas inscritas"]
        self.selected_color = self.content.tui.selected_color
    def preswitch(self):
        pass
    def switch(self):
        self.content.tui.screen.erase()
        self.state = 0
        self.selected = 0
        self.content.pad.erase()
        self.vscrollbar.current = 0
        self.hscrollbar.current = 0

        self.hscrollbar.resize()
        self.vscrollbar.resize()

        self.aulas_inscritas = self.content.tui.logica.db.ListarIncricoesDeAluno(self.aluno)
        self.aulas_inscrever = []
        
        aulas = self.content.tui.logica.db.ListarAulaDeGrupo()

        colsneeded = 0
        
        for aula in aulas:
            incricoes = self.content.tui.logica.db.ListarInscricoesDeAula(aula)
            found = False
            for incricao in incricoes:
                if self.aluno.id == incricao.id:
                    found = True
                    break
            if found or (len(incricoes) + 1) > aula.limit:
                continue
            has_time = True
            for aula_inscrita in self.aulas_inscritas:
                if aula.horainicio <= aula_inscrita.horafinal and aula.horafinal >= aula_inscrita.horafinal:
                    has_time = False
                    break
            if has_time:
                self.aulas_inscrever.append(aula)

        self.content.pad.resize(255, len("Aula: ") + colsneeded + 1 + 200) #-3 = header +1 no caso do terminal não suportar cores +200 - para dar para o texto do estado = 0
    def resize(self):
        self.vscrollbar.resize()
        self.hscrollbar.resize()
    def input(self, ch):
        if self.state == 0:
            if   ch == curses.KEY_LEFT:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif ch == curses.KEY_RIGHT:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif ch == ord("\n"):
                self.state = self.selected + 1
        else:
            if ch == curses.KEY_DOWN and self.vscrollbar.max > 0:
                self.vscrollbar.current = (self.vscrollbar.current + 1) % self.vscrollbar.max
            elif ch == curses.KEY_UP and self.vscrollbar.max > 0:
                self.vscrollbar.current = (self.vscrollbar.current - 1) % self.vscrollbar.max
            elif ch == curses.KEY_RIGHT and self.hscrollbar.needed and (self.hscrollbar.current+1) <= self.hscrollbar.max:
                self.hscrollbar.current = (self.hscrollbar.current + 1)
            elif ch == curses.KEY_LEFT and self.hscrollbar.needed  and 0 <= (self.hscrollbar.current-1) <= self.hscrollbar.max:
                self.hscrollbar.current = (self.hscrollbar.current - 1)
            elif self.state == 1 and ch == ord("\n"):
                if len(self.aulas_inscrever) > 0:
                    aula = self.aulas_inscrever[self.vscrollbar.current]
                    self.content.tui.logica.AdicionarAlunoAaAula(self.aluno, aula)
                    self.aulas_inscritas.append(aula)
                self.switch()
        if ch == curses.KEY_BACKSPACE or ch == curses.ascii.BS:
            self.switch()
    def ver_aulas(self):
        page = self.content.pad
        page.erase()
        txt = f"Aulas inscritas de {self.aluno.nome} ({self.aluno.id})\n"
        page.addstr(txt)
        self.vscrollbar.max = len(self.aulas)
        ### Igual a pagina aulas
        def var_maior(aulas, attr):
            maior = 0
            for i in aulas:
                if attr == "horainicio" or attr == "horafinal":
                    istr = str(getattr(i, attr).strftime("%d/%m/%Y %H:%M"))
                elif attr == "instrutor":
                    instrutor = getattr(i, attr)
                    istr = f"{instrutor.nome} ({instrutor.id})"
                else:
                    istr = str(getattr(i, attr))
                maior = max(maior, len(istr) +2)
            return maior
        attrs = [("Nome","nome"), ("ID", "id"), ("Instrutor", "instrutor"), ("Hora de Início","horainicio"), ("Hora Final", "horafinal"), ("Limite de Alunos","limit")]
        alinhamentos = [c for attr in attrs if(c := var_maior(self.aulas, attr[1]))]
        if len(alinhamentos) > 0:
            for i in range(len(attrs)):
                if len(alinhamentos) == 0:
                    alinhamentos.append(len(attrs[i][0])+2)
                else:
                    alinhamentos[i] = max(alinhamentos[i], len(attrs[i][0])+2)
        else:
            alinhamentos = [len(titulo)+2 for (titulo,_) in attrs]
        
        cols_needed = sum(alinhamentos) + len(attrs) + 1
        page.resize(255, cols_needed)
        
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
        for x in range(start, len(self.aulas)):
            aula = self.aulas[x]
            offset = 2
                
            for i in range(len(attrs)):
                attr = attrs[i][1]
                if attr == "horainicio" or attr == "horafinal":
                    istr = str(getattr(aula, attr).strftime("%d/%m/%Y %H:%M"))
                elif attr == "instrutor":
                    instrutor = getattr(aula, attr)
                    istr = f"{instrutor.nome} ({instrutor.id})"
                else:
                    istr = str(getattr(aula, attr))
                page.addstr(line, offset, istr)
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
    def increver(self):
        page = self.content.pad
        txt = f"Inscrever {self.aluno.nome} ({self.aluno.id}) em aula\n"
        page.addstr(txt)
        page.addstr("Aula: ")
        line, cursorx = page.getyx()
        self.vscrollbar.max = len(self.aulas_inscrever)

        for i in range(self.vscrollbar.current, len(self.aulas_inscrever)):
            aula = self.aulas_inscrever[i]
            color = 0
            if self.vscrollbar.current == i:
                if curses.has_colors():
                    color = self.selected_color
                else:
                    page.addch(line, cursorx-1, 'X')
            page.addstr(line, cursorx, f"{aula.nome} ({aula.id}) - {aula.horainicio.strftime("%d/%m/%Y %H:%M")} -> {aula.horafinal.strftime("%d/%m/%Y %H:%M")}", color)
            if self.vscrollbar.current == i and not curses.has_colors():
                page.addch('X')
            line+=1
            if line >= 254:
                break
        self.vscrollbar.render()
        self.hscrollbar.render()
    def render(self):
        page = self.content.pad
        page.erase()
        if self.state == 0:
            page.addstr(f"{self.aluno.nome} ({self.aluno.id})\n")
            page.move(1,0)
            for i in range(len(self.buttons)):
                attr = 0
                if self.selected == i:
                    attr = curses.A_BOLD
                page.addstr(f" {self.buttons[i]} ", attr)
        elif self.state == 1:
            self.increver()
        elif self.state == 2:
            self.ver_aulas()
    def refresh(self):
        self.content.pad.refresh(0,0,3,0, self.content.maxlines-1, self.content.maxcols-1)