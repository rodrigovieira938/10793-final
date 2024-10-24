from ._tui import Tui
import curses
import math

class Scrollbar:
    def __init__(self, tui: Tui, vertical : bool):
        self.needed = False
        self.vertical = vertical
        self.max = 255
        self.current = 0
        self.maxcols = tui.maxcols
        self.maxlines = tui.maxlines
        self.tui = tui

        if vertical:
            self.window = curses.newpad(self.maxlines-3, 1)
        else:
            self.window = curses.newpad(1, self.maxcols-1)
    def resize(self):
        self.maxlines = self.tui.maxlines
        self.maxcols = self.tui.maxcols
        if self.vertical:
            self.window.resize(self.maxlines-3, 1)
    def render(self):
        self.window.erase()
        if not self.needed or self.max == 0:
            return
        if self.vertical:
            for i in range(self.maxlines-4):
                self.window.addch("█")
            line = min(math.floor((self.current*self.maxlines)/self.max), self.maxlines-5)
            self.window.addch(line,0,"X")
            self.window.refresh(0,0,3,self.maxcols-1, self.maxlines-1, self.maxcols-1)
        else:
            for i in range(self.maxcols-2):
                self.window.addch("█")
            col = min(math.floor((self.current*self.maxcols)/self.max), self.maxcols-3)
            self.window.addch(0, col, "X")
            self.window.refresh(0,0,self.maxlines-2,0,self.maxlines-2, self.maxcols-2)