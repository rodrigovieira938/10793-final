from .content import Content, curses

class PagAulas:
    def __init__(self, content : Content):
        self.content = content
    def preswitch(self):
        pass
    def switch(self):
        pass
    def render(self):
        self.content.pad.addstr("Quinta página\n")