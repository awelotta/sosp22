from plumbum import colors, cli
from pyfiglet import Figlet
import yaml, ruamel.yaml
import os
import fnmatch
import questionary
import textwrap
from datetime import datetime

author = ""
journal_name = ""
       
def save_config(filename, config):
    yaml = ruamel.yaml.YAML()
    with open(filename, 'w') as file: # 'with' keyword automatically handles file.close()
        yaml.dump(config, file)

def load_config(filename):
    global author, journal_name
    if not os.path.exists(filename):
        save_config(filename, {
            "author": "",
            "journal_name": "",
        })
    with open(filename, 'r') as file:
        data = yaml.safe_load(file) # safe_load returns a map with the same thing. yaml is basically a json (i think there is some overlap)
    author = data["author"]
    journal_name = data["journal_name"]
        
def print_banner(text):
    with colors['WHEAT1']:
        print(Figlet(font='rozzo').renderText(text))

class GrttdeJrnl(cli.Application):
    VERSION = "0.0"
    def main(self):
        print_banner(f'Welcome to {__class__.__name__}')
        load_config("config.yaml")
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                'Write journal entry',
                'Read journal entries',
                'Quit'
        ]).ask()
        if choice == 'Write journal entry':
            if journal_name == "":
                create_journal()
            open_journal()
        elif choice == 'Read journal entries':
            read_entries()
        elif choice == 'Quit':
            pass

def open_journal():
    today_entry = str(datetime.today().strftime('%Y-%m-%d'))+".txt"
    os.chdir(journal_name)
    entry_list = os.listdir()
    if not entry_list:
        add_page(today_entry)
    else:
        match_exists = False # different from their implementation
        for entry in entry_list:
            if fnmatch.fnmatch(entry, today_entry):
                match_exists = True
                add_content(today_entry)
                break
        if not match_exists:
            add_page(today_entry)
    
def add_page(entry):
    open(entry, 'x')
    print("Created Entry " + entry)
    add_content(entry)

def add_content(filename):
    with open(filename, 'a') as file:
        input = questionary.text("What are you grateful for?", multiline=True).ask()
        pretty_input = textwrap.fill(input) + '\n'
        file.write(pretty_input)

def read_entries():
    os.chdir(journal_name)
    journal_list = os.listdir()
    question = [{
        "type": "select",
        "name": "select_entry",
        "message": "Choose an entry to read",
        "choices": journal_list
    },]
    entry = questionary.prompt(question)['select_entry']
    with open(entry, 'r') as e:
        print(e.read())

def create_journal():
    global author, journal_name
    author = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is your name?").ask())
    journal_name = ruamel.yaml.scalarstring.DoubleQuotedScalarString(author+"-journal")
    config_dict = dict(author=author, journal_name=journal_name)
    save_config("config.yaml", config_dict)
    init_folder(journal_name)

def init_folder(folder_name):
    try:
        os.makedirs(folder_name)
    except OSError:
        print(f"Creating the director {folder_name} has failed")
    # os.chdir(journal_name)
    open_journal()

if __name__ == "__main__":
    GrttdeJrnl()