from plumbum import cli, colors
from pyfiglet import Figlet

import lib

class App(cli.Application):
    # https://plumbum.readthedocs.io/en/latest/_modules/plumbum/cli/application.html for meta switches and class-level attributes
    PROGNAME = "Awelottado"
    VERSION = "0.0"
    DESCRIPTION = "A menu-based command line app for ineffectively manipulating a very simple (todo) list. Uses the `questionary` Python module."
    USAGE = "Run with no arguments to view the menus. The todo list itself is stored in `data/todo.txt`, and the done list is stored in `data/done.txt`."
  
    def main(self):
        welcome_message()
        lib.menu()

def welcome_message():
    with colors['WHEAT1']:
        print(Figlet(font='slant').renderText(App.PROGNAME))
        print(f"Welcome to {App.PROGNAME}, a questionary powered CLI for manipulating a (todo) list")

if __name__ == "__main__":
    App()
