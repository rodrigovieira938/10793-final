from .tui import Tui
import sys
import curses

def run():
    ### Rederecionar o output para um ficheiro
    f = open("log.txt", "w")
    sys.stdout = f
    ###
    tui = Tui()
    curses.wrapper(tui.init)