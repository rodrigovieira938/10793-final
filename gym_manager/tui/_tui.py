import curses
import sys
from ..logica import Logica

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

        self.windows = {
            TAB_WINDOW: Header(self), 
            CONTENT_WINDOW: Content(self),
        }
        self.__run()

    def __run(self):
        try:
            while self.running == True:
                ch = self.screen.getch()
                if ch == curses.KEY_F1:
                    self.running = False
                elif ch == curses.KEY_RESIZE:
                    self.maxlines, self.maxcols = self.screen.getmaxyx()
                    curses.resize_term(self.maxlines, self.maxcols)
                    self.screen.resize(self.maxlines, self.maxcols)
                    self.screen.erase()
                    for (_, w) in self.windows.items():
                        w.resize()
                elif ch == ord("\t"):
                    self.windows[CONTENT_WINDOW].preswitch(self.windows[TAB_WINDOW].selected)
                    self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected + 1) % len(self.windows[TAB_WINDOW].tabs)
                    self.screen.erase()
                    self.windows[CONTENT_WINDOW].switch(self.windows[TAB_WINDOW].selected)
                else:
                    self.windows[CONTENT_WINDOW].input(ch)
                for (_, window) in self.windows.items():
                    window.render()
        except KeyboardInterrupt:
            curses.endwin()

    def __resize(self, lines, cols):
        curses.resize_term(lines, cols)
        self.screen.resize(lines, cols)
        self.screen.erase()
        for (_, w) in self.windows.items():
            w.resize(lines, cols)
            w.clear()
