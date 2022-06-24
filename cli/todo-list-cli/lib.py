import questionary as qy
import os
import textwrap

TODO_PATH="data/todo.txt"
DONE_PATH="data/done.txt"

def menu():
    clean(DONE_PATH)
    clean(TODO_PATH)
    with open(TODO_PATH, 'r') as f: todo_len = len(f.read())
    with done(TODO_PATH, 'r') as f: done_len = len(f.read())
    choice = qy.select(
        "Menu",
        choices = [
            'add tasks',
            qy.Choice("browse todo list and complete tasks",   disabled="todo list is currently empty" if todo_len == 0 else None, value='browse todo'),
            qy.Choice("browse todo list and reorder tasks",    disabled="todo list is currently empty" if todo_len == 0 else None, value='reorder todo'),
            qy.Choice("browse done list and uncomplete tasks", disabled="done list is currently empty" if done_len == 0 else None, value='browse done'),
            'quit'
        ]
    ).ask()
    if choice == 'add tasks': # could use a dictionary and list comprehension and locals()... poo
        add_tasks()
    elif choice == 'browse todo':
        browse_todo()
    elif choice == 'reorder todo':
        reorder_todo()
    elif choice == 'browse done':
        browse_done()

def add_tasks():
    choice = qy.select(
        "Prepend or append to todo list?",
        choices = [
            'prepend',
            'append',
        ]
    ).ask()
    input = qy.text(
        "You may beging writing. Individual tasks go on individual lines. Empty lines will be ignored.", multiline=True
    ).ask() + '\n' # should files end with a newline?
    if choice == 'prepend':
        prepend(TODO_PATH, input)
    elif choice == 'append':
        append(TODO_PATH, input)
    print(f"{TODO_PATH} modified")
    menu()

def prepend(filename, input):
    with open(filename, 'r') as original: data = original.read()
    with open(filename, 'w') as modified: modified.write(input + data)

def append(filename, input):
    with open(filename, 'a') as modified: modified.write('\n'+input)
   
def browse_todo():
    browse_and_transfer(TODO_PATH, DONE_PATH, "Select items to archive, or select nothing to do nothing")

def reorder_todo():
    qy.print(
        "Select exactly two lines that you want to swap the positions of, or select nothing to stop finish"
    )
    reorder_todo_main_loop()

def reorder_todo_main_loop():
    with open(TODO_PATH, 'r') as f:
        enumerated_tasks = [
            (n, t) for (n, t) in enumerate(f.read().split('\n'))
        ]
    to_swap = qy.checkbox(
        "",
        choices=[qy.Choice(t, value=n) for (n, t) in enumerated_tasks],
        validate=
            lambda selection: True if (len(selection) == 2 or len(selection) == 0) else
                "Please select exactly two lines, or zero lines to go back to the menu"
    ).ask()
    if len(to_swap) == 0: # doesn't work if you put, if not to_swap
        menu()
    else:
        i, j = to_swap
        enumerated_tasks[i], enumerated_tasks[j] = enumerated_tasks[j], enumerated_tasks[i]
        output = '\n'.join([t for (n, t) in enumerated_tasks])
        with open(TODO_PATH, 'w') as todo: todo.write(output)
        reorder_todo_main_loop()

def browse_done():
    browse_and_transfer(DONE_PATH, TODO_PATH, "Select files to uncomplete or select nothing to do nothing")

def browse_and_transfer(browse_file, other_file, prompt_text):
    with open(browse_file, 'r') as f:
        enumerated_tasks = [
            (n, t) for (n, t) in enumerate(f.read().split('\n'))
        ] # but i would also like to clean the todo list? but it might be desired by the user to have keep empty lines that are simply ignored
    to_archive = qy.checkbox(
        prompt_text,
        choices=[qy.Choice(t, value=n) for (n, t) in enumerated_tasks if t and not t.isspace()]
    ).ask()
    archived_tasks = [t for (n, t) in enumerated_tasks if n in to_archive and t and not t.isspace()]
    archived_text = '\n'.join(archived_tasks)
    append(other_file, archived_text)
    modified_tasks = [t for (n, t) in enumerated_tasks if n not in to_archive] # seems inefficient to loop twice
    modified_text = '\n'.join(modified_tasks)
    qy.print(modified_text) # style= ??? i want same as other prompt color
    with open(browse_file, 'w') as todo: todo.write(modified_text)
    menu()

def clean(file):
    with open(file, 'r') as f: data = f.read().split('\n')
    data = [x for x in data if x and not x.isspace()]
    output = '\n'.join(data)
    with open(file, 'w') as f: f.write(output)
    