import curses.ascii
from .content import Content, curses
from .scrollbar import Scrollbar
from ._tui import Tui
from ..AulaGrupo import Aulasgrupo
import datetime

PLACEHOLDER_ANY = 0
PLACEHOLDER_NUMBER = 2
PLACEHOLDER_CELLPHONE = 3
PLACEHOLDER_EMAIL = 4
PLACEHOLDER_DATE = 5
PLACEHOLDER_HOUR = 6
PLACEHOLDER_INSTRUTOR_COMBO = 7

class Placeholder:
    def __init__(self, placeholder, type):
        self.placeholder = placeholder
        self.type = type

class TextInput:
    def __init__(self, placeholders : list[Placeholder], pad, tui : Tui):
        self.placeholders = placeholders
        self.state = 0
        self.pad = pad
        self.strs = []
        self.str = ""
        self.vscrollbar = Scrollbar(tui, True)
        self.tui = tui
        self.instrutores = []

    def resize(self):
        self.maxlines, self.maxcols = self.pad.getmaxyx()
    def instrutores_disponiveis(self):
        self.instrutores = []
        instrutores = self.tui.logica.db.ListarInstrutores()
        
        dia = int(self.strs[2][0:2])
        mes = int(self.strs[2][3:5])
        ano = int(self.strs[2][6:])
        hora_comeco   = int(self.strs[3][0:2])
        minuto_comeco = int(self.strs[3][3:])
        hora_final   = int(self.strs[4][0:2])
        minuto_final = int(self.strs[4][3:])

        hora_inicial = datetime.datetime(ano, mes, dia, hora_comeco, minuto_comeco)
        hora_acabar = datetime.datetime(ano, mes, dia, hora_final, minuto_final)

        if hora_acabar <= hora_inicial:
            hora_acabar += datetime.timedelta(days=1)

        for instrutor in instrutores:
            has_time = True
            for aula in self.tui.logica.db.ListartAulaDeInstrutor(instrutor):
                if hora_inicial <= aula.horafinal and hora_acabar >= aula.horafinal:
                    has_time = False
                    break
            if has_time:
                self.instrutores.append(instrutor)
        self.vscrollbar.max = len(self.instrutores)
    def render(self):
        if self.state < len(self.placeholders):
            if self.placeholders[self.state].type != PLACEHOLDER_INSTRUTOR_COMBO:
                self.pad.addstr(f" {self.placeholders[self.state].placeholder}: {self.str}")
            else:
                page = self.pad
                self.pad.addstr(f" {self.placeholders[self.state].placeholder}: ")
                line, cursorx = page.getyx()
                self.instrutores_disponiveis()
                for i in range(self.vscrollbar.current, len(self.instrutores)):
                    instrutor = self.instrutores[i]
                    color = 0
                    if self.vscrollbar.current == i:
                        if curses.has_colors():
                            color = self.tui.selected_color
                        else:
                            page.addch(line, cursorx-1, 'X')
                    page.addstr(line, cursorx, f"{instrutor.nome} ({instrutor.id})", color)
                    if self.vscrollbar.current == i and not curses.has_colors():
                        page.addch('X')
                    line+=1
                    if line >= 254:
                        break
                self.vscrollbar.render()
            return False
        
        return True
    def next_input(self):
        self.strs.append(self.str)
        self.str = ""
        self.state += 1
    def input(self,ch):
        if self.state >= len(self.placeholders):
            return
        
        type = self.placeholders[self.state].type

        if ch == curses.KEY_BACKSPACE or ch == curses.ascii.BS:
            self.str = self.str[:-1]
        elif ch == ord("\n"):
            if type == PLACEHOLDER_CELLPHONE:
                size_needed = 9
                if self.str.startswith("+"):
                    size_needed += 4
                if len(self.str) == size_needed:
                    self.next_input()
            elif type == PLACEHOLDER_EMAIL:
                if self.str.count("@") > 0 and self.str[-1] != "@":
                    self.next_input()
            elif type == PLACEHOLDER_DATE:
                if len(self.str) == len("xx/xx/xxxx"):
                    self.next_input()
            elif type == PLACEHOLDER_HOUR:
                if len(self.str) == len("xx:xx"):
                    self.next_input()
            elif type == PLACEHOLDER_INSTRUTOR_COMBO:
                if len(self.instrutores) > 0:
                    self.next_input()
            elif type == PLACEHOLDER_NUMBER:
                if len(self.str) > 0:
                    try:
                        n = int(self.str)
                        if n != 0:
                            self.next_input()
                    except Exception:
                        pass
            else:
                if len(self.str) > 0:
                    self.next_input()
            return
        if type == PLACEHOLDER_ANY:
            if curses.ascii.isgraph(ch) or ch == ord(' '): #isgraph() = todos os caracteres printaveis sem ser espaços
                self.str += curses.ascii.unctrl(ch)
        elif type == PLACEHOLDER_NUMBER:
            if curses.ascii.isdigit(ch):
                self.str += curses.ascii.unctrl(ch)
        elif type == PLACEHOLDER_CELLPHONE:
            if len(self.str) == 0 and curses.ascii.unctrl(ch) == "+":
                self.str += "+"
            elif curses.ascii.isdigit(ch):
                self.str += curses.ascii.unctrl(ch)
        elif type == PLACEHOLDER_EMAIL: 
            if self.str.count("@") == 0: # https://en.wikipedia.org/wiki/Email_address#Local-part
                if curses.ascii.isalnum(ch) or curses.ascii.unctrl(ch) in "!#$%&'*+-/=?^_`{|}~.@":
                    if curses.ascii.unctrl(ch) == "." and self.str[-1] != '.' and len(self.str) > 0:
                        self.str += "."
                    else:
                        self.str += curses.ascii.unctrl(ch)
            else:
                if curses.ascii.isalnum(ch) or curses.ascii.unctrl(ch) in '[]-.': # https://en.wikipedia.org/wiki/Email_address#Domain
                    self.str += curses.ascii.unctrl(ch)
        elif type == PLACEHOLDER_DATE:
            if   len(self.str) == 0: #parte do dia
                if ch in [ord("0"), ord("1"), ord("2"), ord("3")]:
                    self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 1:
                if self.str[0] == "0":
                    if ch in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                        self.str += curses.ascii.unctrl(ch)
                elif  self.str[0] == "1" or self.str[0] == "2":
                    if ch in [ord("0"), ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                        self.str += curses.ascii.unctrl(ch)
                else:
                    if ch in [ord("0"), ord("1")]:
                        self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 3: #parte do mes
                if ch in [ord("0"), ord("1")]:
                        self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 4:
                if self.str[3] == "1":
                    if ch in [ord("0"), ord("1"), ord("2")]:
                            self.str += curses.ascii.unctrl(ch)
                else:
                    if ch in [ord("1"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                        self.str += curses.ascii.unctrl(ch)
                    elif ch == ord("2") and int(self.str[0:2]) <= 29:
                        self.str += curses.ascii.unctrl(ch)
            elif 6 <= len(self.str) <= 8: #parte do ano
                if ch in [ord("0"), ord("1"),ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                        self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 9:
                # xx/xx/xxx
                dia = int(self.str[0:2])
                mes = int(self.str[3:5])
                if not ch in [ord("0"), ord("1"),ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                    return
                ano = int(self.str[6:] + curses.ascii.unctrl(ch))
                if mes != 2 or (mes == 2 and dia <= 28):
                    self.str += curses.ascii.unctrl(ch)
                else: # dia 29/2
                    if (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0: # formula para saber se o ano é bissexto https://pt.wikihow.com/Descobrir-se-um-Ano-%C3%A9-Bissexto
                        self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 2 or len(self.str) == 5: 
                if ch == ord("/"):
                    self.str += "/"
        elif type == PLACEHOLDER_HOUR:
            # xx:xx
            if len(self.str) == 0: # parte da hora
                if ch in [ord("0"), ord("1"), ord("2")]:
                    self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 1:
                if self.str[0] == "0":
                    if ch in [ord("1"),ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                        self.str += curses.ascii.unctrl(ch)
                elif self.str[0] == "1":
                    if ch in [ord("0"), ord("1"),ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                        self.str += curses.ascii.unctrl(ch)
                elif self.str[0] == "2":
                    if ch in [ord("0"), ord("1"),ord("2"), ord("3")]:
                        self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 2: #separador
                if ch == ord(":"):
                    self.str += ":"
            elif len(self.str) == 3:
                if ch in [ord("0"), ord("1"),ord("2"), ord("3"), ord("4"), ord("5")]:
                    self.str += curses.ascii.unctrl(ch)
            elif len(self.str) == 4:
                if ch in [ord("0"), ord("1"),ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
                    self.str += curses.ascii.unctrl(ch)
                pass
        elif type == PLACEHOLDER_INSTRUTOR_COMBO:
            if ch == curses.KEY_DOWN and self.vscrollbar.max > 0:
                self.vscrollbar.current = (self.vscrollbar.current + 1) % self.vscrollbar.max
            elif ch == curses.KEY_UP and self.vscrollbar.max > 0:
                self.vscrollbar.current = (self.vscrollbar.current - 1) % self.vscrollbar.max

    def cols_needed(self):
        if self.placeholders[self.state].type != PLACEHOLDER_INSTRUTOR_COMBO:
            return len(f" {self.placeholders[self.state].placeholder}: {self.str}")
        return self.pad.getmaxyx()[1]-200
class TimedMessage:
    def __init__(self,msg, seconds, pad):
        self.startTime = datetime.datetime.now()
        self.endTime = self.startTime + datetime.timedelta(seconds=seconds)
        self.msg = msg
        self.pad = pad
    def render(self):
        if(datetime.datetime.now() <= self.endTime):
            self.pad.addstr(f" {self.msg}")
            return False
        else:
            return True
# Estados:
# 0 - selecionar o que registrar
# 1 - registrar aluno
# 2 - registrar instrutor
# 3 - registrar aula de grupo
class PagRegistrar:
    def __init__(self, content : Content):
        self.content = content
        self.selected = 0
        self.buttons = ["Registrar Aluno","Registrar Instrutor", "Registrar Aula de Grupo"]
        self.state = 0
        self.textinput = None
        self.hscrollbar = Scrollbar(self.content.tui, False)
    def preswitch(self):
        self.state = 0
        self.selected = 0
    def switch(self):
        self.content.pad.erase()
        self.resize()
        instrutores =  self.content.tui.logica.db.ListarInstrutores()
        maxcols = 0
        for instrutor in instrutores:
            maxcols = max(maxcols, len(f"{instrutor.nome} ({instrutor.id})"))
        self.content.pad.resize(255,maxcols+200) #+200 para dar espaço para o placeholder e os butões do estado = 0
    def resize(self):
        self.hscrollbar.resize()
    def input(self, ch):
        if self.state == 0:
            if   ch == curses.KEY_LEFT:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif ch == curses.KEY_RIGHT:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif ch == ord("\n"):
                self.state = self.selected + 1
                if self.state == 1 or self.state == 2:
                    self.textinput = TextInput([Placeholder("Introduza o nome",PLACEHOLDER_ANY), Placeholder("Introduza o contacto", PLACEHOLDER_CELLPHONE), Placeholder("Introduza o Email", PLACEHOLDER_EMAIL), Placeholder("Introduza a Morada", PLACEHOLDER_ANY), Placeholder("Introduza a Idade", PLACEHOLDER_NUMBER)], self.content.pad, self.content.tui)
                else:
                    self.textinput = TextInput([Placeholder("Introduza o nome", PLACEHOLDER_ANY), Placeholder("Introduza o limite de alunos", PLACEHOLDER_NUMBER), Placeholder("Introduza o dia", PLACEHOLDER_DATE), Placeholder("Introduza a hora do começo", PLACEHOLDER_HOUR), Placeholder("Introduza a hora do final", PLACEHOLDER_HOUR), Placeholder("Introduza o instrutor", PLACEHOLDER_INSTRUTOR_COMBO)], self.content.pad, self.content.tui)
        else:
            if   ch == curses.KEY_LEFT and self.hscrollbar.current - 1 >= 0:
                self.hscrollbar.current -= 1
            elif ch == curses.KEY_RIGHT and self.hscrollbar.current + 1 <= self.hscrollbar.max:
                self.hscrollbar.current += 1
            else:
                if self.textinput is not None:
                    self.textinput.input(ch)
    
    def render(self):
        page = self.content.pad
        page.erase()
        page.move(1,0)
        if self.state == 0:
            for i in range(len(self.buttons)):
                attr = 0
                if self.selected == i:
                    attr = curses.A_BOLD
                page.addstr(f" {self.buttons[i]} ", attr)
        elif self.state == 1 or self.state == 2:
            if self.state == 1:
                page.addstr("Criar aluno\n")
            else:
                page.addstr("Criar Instrutor\n")
            page.addch("\n")
            if self.textinput.render():
                if self.state == 1:
                    self.content.tui.logica.CriarUtilizador(self.textinput.strs[0], self.textinput.strs[1], self.textinput.strs[2], self.textinput.strs[3], int(self.textinput.strs[4]))
                else:
                    self.content.tui.logica.CriarInstructor(self.textinput.strs[0], self.textinput.strs[1], self.textinput.strs[2], self.textinput.strs[3], int(self.textinput.strs[4]))
                self.textinput = None
                self.state = 0
            else:
                cols_needed = self.textinput.cols_needed()
                max_cols = self.content.tui.maxcols
                dif = cols_needed - max_cols
                self.hscrollbar.max = max(dif,0)
                self.hscrollbar.needed = self.hscrollbar.max != 0 
        else:
            page.addstr("Criar Aula\n\n")
            if self.textinput.render():
                dia = int(self.textinput.strs[2][0:2])
                mes = int(self.textinput.strs[2][3:5])
                ano = int(self.textinput.strs[2][6:])
                hora_comeco   = int(self.textinput.strs[3][0:2])
                minuto_comeco = int(self.textinput.strs[3][3:])
                hora_final   = int(self.textinput.strs[4][0:2])
                minuto_final = int(self.textinput.strs[4][3:])

                hora_inicial = datetime.datetime(ano, mes, dia, hora_comeco, minuto_comeco)
                hora_acabar = datetime.datetime(ano, mes, dia, hora_final, minuto_final)
                
                if hora_acabar <= hora_inicial:
                    hora_acabar += datetime.timedelta(days=1)

                self.content.tui.logica.CriarAulaDeGrupo(self.textinput.strs[0], self.textinput.instrutores[self.textinput.vscrollbar.current], hora_inicial, hora_acabar, self.textinput.strs[1])
            
                self.textinput = None
                self.state = 0
            else:
                cols_needed = self.textinput.cols_needed()
                max_cols = self.content.tui.maxcols
                dif = cols_needed - max_cols
                self.hscrollbar.max = max(dif,0)
                self.hscrollbar.needed = self.hscrollbar.max != 0 
        self.hscrollbar.render()
    def refresh(self):
        offset = self.hscrollbar.current
        self.content.pad.refresh(0,offset,3,0, self.content.maxlines-3, self.content.maxcols-1) # -1 para o limite -2 para a scrollbar e o espaço em branco
        self.hscrollbar.refresh()