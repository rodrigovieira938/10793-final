from .content import Content, curses

class PagInstrutor:
    def __init__(self, content : Content):
        self.content = content
    def preswitch(self):
        pass
    def switch(self):
        pass
    def resize(self):
        pass
    def input(self, ch):
        pass
    def render(self):
        self.content.pad.addstr("Quarta página\n")
    def refresh(self):
        self.content.pad.refresh(0,0,3,0, self.content.maxlines-1, self.content.maxcols-1)