import curses
import sys
TAB_WINDOW = "TAB"
CONTENT_WINDOW = "CONTENT"
VERTICAL_SCROLLBAR = "VSCROLLBAR"
HORIZONTAL_SCROLLBAR = "HSCROLLBAR"

class Tui:
    def init(self, screen):
        from .header import Header
        from .content import Content
        from .scrollbar import Scrollbar
        self.screen = screen     
        self.running = True
        self.maxlines, self.maxcols = self.screen.getmaxyx() 

        self.screen.nodelay(1)
        curses.curs_set(0)

        self.windows = {
            TAB_WINDOW: Header(self), 
            CONTENT_WINDOW: Content(self),
            VERTICAL_SCROLLBAR: Scrollbar(self, True),
            HORIZONTAL_SCROLLBAR: Scrollbar(self, False)
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
                    self.windows[TAB_WINDOW].selected = (self.windows[TAB_WINDOW].selected + 1) % len(self.windows[TAB_WINDOW].tabs)
                elif ch == curses.KEY_DOWN:
                    self.windows[VERTICAL_SCROLLBAR].current = (self.windows[VERTICAL_SCROLLBAR].current + 1) % self.windows[VERTICAL_SCROLLBAR].max
                elif ch == curses.KEY_UP:
                    self.windows[VERTICAL_SCROLLBAR].current = (self.windows[VERTICAL_SCROLLBAR].current - 1) % self.windows[VERTICAL_SCROLLBAR].max
                elif ch == curses.KEY_RIGHT:
                    self.windows[HORIZONTAL_SCROLLBAR].current = (self.windows[HORIZONTAL_SCROLLBAR].current + 1) % self.windows[HORIZONTAL_SCROLLBAR].max
                elif ch == curses.KEY_LEFT:
                    self.windows[HORIZONTAL_SCROLLBAR].current = (self.windows[HORIZONTAL_SCROLLBAR].current - 1) % self.windows[HORIZONTAL_SCROLLBAR].max
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