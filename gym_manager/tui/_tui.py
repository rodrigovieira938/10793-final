import curses
import sys
from ..logica import Logica
import time

TAB_WINDOW = "TAB"
CONTENT_WINDOW = "CONTENT"

class Tui:
    def init(self, screen):
        from .header import Header
        from .content import Content
        self.screen = screen     
        self.running = True
        self.maxlines, self.maxcols = self.screen.getmaxyx() 
        self.logica = Logica()

        self.screen.nodelay(1)
        curses.curs_set(0)

        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            self.selected_color = curses.color_pair(1)

        self.windows = {
            TAB_WINDOW: Header(self), 
            CONTENT_WINDOW: Content(self),
        }

#        for i in range(300):
#            import datetime
#            user1 = self.logica.CriarUtilizador(f"Aluno {i+1}", "111111111", f"aluno.{i+1}@gmail.com", f"Rua das Ruas {i+1}", 20)
#            inst1 = self.logica.CriarInstructor(f"Instrutor {i+1}", "111111111", f"instrutor.{i+1}@gmail.com", f"Rua das Ruas {i+1}", 20)
#            aula1 = self.logica.CriarAulaDeGrupo(f"Aula {i+1}", inst1, datetime.datetime.now() + datetime.timedelta(hours=1), datetime.datetime.now() + datetime.timedelta(hours=2), 20)
#            self.logica.AdicionarAlunoAaAula(user1, aula1)

        self.__run()

    def __run(self):
        try:
            while self.running == True:
                ch = self.screen.getch()
                if ch == curses.KEY_F1:
                    self.running = False
                elif ch == curses.KEY_RESIZE:
                    self.maxlines, self.maxcols = self.screen.getmaxyx()
                    self.__resize(self.maxlines, self.maxcols)
                elif ch == ord("\t"):
                    if self.windows[TAB_WINDOW].selected < len(self.windows[TAB_WINDOW].tabs): # Existe mais tabs do que as que aparecem
                        self.windows[CONTENT_WINDOW].preswitch(self.windows[TAB_WINDOW].selected)
                        self.windows[TAB_WINDOW].selected_before = self.windows[TAB_WINDOW].selected
                        self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected + 1) % len(self.windows[TAB_WINDOW].tabs)
                        self.screen.erase()
                        self.windows[CONTENT_WINDOW].switch(self.windows[TAB_WINDOW].selected)
                    else:
                        self.windows[CONTENT_WINDOW].preswitch(self.windows[TAB_WINDOW].selected_before)
                        self.windows[TAB_WINDOW].selected = self.windows[TAB_WINDOW].selected_before
                        self.windows[CONTENT_WINDOW].switch(self.windows[TAB_WINDOW].selected_before)
                        self.windows[TAB_WINDOW].selected_before = 0
                        pass
                else:
                    self.windows[CONTENT_WINDOW].input(ch)
                for (_, window) in self.windows.items():
                    #try:
                    window.render()
                    #except Exception:
                    #    self.maxlines, self.maxcols = self.screen.getmaxyx()
                    #    self.__resize(self.maxlines, self.maxcols)
                time.sleep(1/60) #60 fps
        except KeyboardInterrupt:
            pass

    def __resize(self, lines, cols):
        curses.resize_term(lines, cols)
        self.screen.resize(lines, cols)
        self.screen.erase()
        self.maxcols = cols
        self.maxlines = lines
        for (_, w) in self.windows.items():
            w.resize()
