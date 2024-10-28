from ._tui import Tui
import curses
import math

class Scrollbar:
    def __init__(self, tui: Tui, vertical : bool):
        self.needed = False
        self.vertical = vertical
        self.max = 0
        self.current = 0
        self.maxcols = tui.maxcols
        self.maxlines = tui.maxlines
        self.tui = tui

        if vertical:
            self.pad = curses.newpad(self.maxlines-3, 1) #-3 pelo tamanho do header
        else:
            self.pad = curses.newpad(1, self.maxcols-2) #-2 para não bater no scrollbar vertical
    def resize(self):
        self.maxlines = self.tui.maxlines
        self.maxcols = self.tui.maxcols
        self.pad.erase()
        if self.vertical:
            self.pad.resize(self.maxlines-3, 1)
        else:
            self.pad.resize(1, self.maxcols-2)
    def render(self):
        self.pad.erase()
        sy, sx = self.pad.getmaxyx()

        if self.needed == False or self.max == 0:
            return
        if self.vertical:
            for i in range(sy-1):
                self.pad.addch("█")
            line = min(math.floor((self.current*self.maxlines)/self.max), sy-2) # -1 pelo limite e -1 porque as llinhas começam a contar do 0
            self.pad.addch(line,0,"X")
        else:
            for i in range(sx-1):
                self.pad.addch("█")
            col = min(math.floor((self.current*self.maxcols)/self.max), sx-2)
            self.pad.addch(0, col, "X")
    def refresh(self):
        if self.vertical:
            self.pad.refresh(0,0,3,self.maxcols-2, self.maxlines-1, self.maxcols-1)
        else:
            self.pad.refresh(0,0,self.maxlines-1,0,self.maxlines-1, self.maxcols-1)
