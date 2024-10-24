from .content import Content, curses

class PagRegistrar:
    def __init__(self, content : Content):
        self.content = content
    def preswitch(self):
        pass
    def switch(self):
        self.content.pad.erase()
        self.resize()
    def resize(self):
        self.content.pad.resize(self.content.maxlines, self.content.maxcols)
    def input(self, ch):
        pass
    def render(self):
        self.content.pad.addstr("Segunda página\n")
    def refresh(self):
        self.content.pad.refresh(0,0,3,0, self.content.maxlines-1, self.content.maxcols-1)