import pygame as pg
import pygame.freetype as ft
import sys, random, string
import itertools
import functools
from collections import deque
import statistics

print("Starting...")
pg.init()
ft.init()
resolution = (800, 800) # width, height; top-left = (0,0)
screen = pg.display.set_mode(resolution)

STAGE_BG_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
BG_COLOR = (255,255,255)
PLAYER_COLOR = (30,58,232)

class Stage(pg.sprite.Sprite): # maybe I should implement this better, i.e. as a group
    def __init__(self):
        super().__init__()
        margin = 30
        self.rect = pg.Rect(margin, margin,
            resolution[0] - 2*margin, resolution[1] - 2*margin)
        self.grid_shape = (10, 10) # w, h # I should rework this. pg.Rect is W/H so that's the convention I'll use.
        self.letters = list()
        letters_as_strings = Stage.generate_grid(self.grid_shape)
        self.letter_width  = self.rect.width  / self.grid_shape[0] # ah, but I could be getting the width of the letter.rect.. wev
        self.letter_height = self.rect.height / self.grid_shape[1]
        self.letters = [
            [
                Letter(lt,
                       self.rect.left + self.letter_width*r, self.rect.top + self.letter_width*c,
                       self.letter_width, self.letter_height
                ) for c, lt in enumerate(row)
            ] for r, row in enumerate(letters_as_strings) # yummy list comprehension owo
        ]
        self.image = pg.Surface((self.rect.width, self.rect.height)) # idk mannn11nn1n
        self.image.fill(STAGE_BG_COLOR)

    def generate_grid(shape): # shape is (x/c/w, y/r/h) # I think this works
        grid = [ # initial guess
            [
                random.choice(string.ascii_lowercase) for i in range(shape[0])
            ] for i in range(shape[1])
        ]
        for r in range(shape[1]):
            for c in range(shape[0]): # assume square
                # basically a diamond structure: where all the A's are potential conflicts
                # ..A..
                # .A.A.
                # A.X.A
                # .A.A.
                # ..A..
                conflicts = { # I could do this fancy, but I won't
                    grid[r-2][c  ] if r-2 in range(shape[1])                            else None,
                    grid[r-1][c-1] if r-1 in range(shape[1]) and c-1 in range(shape[0]) else None,
                    grid[r-1][c+1] if r-1 in range(shape[1]) and c+1 in range(shape[0]) else None,
                    grid[r  ][c-2] if                            c-2 in range(shape[0]) else None,
                    grid[r  ][c+2] if                            c+2 in range(shape[0]) else None,
                    grid[r+1][c-1] if r+1 in range(shape[1]) and c-1 in range(shape[0]) else None,
                    grid[r+1][c+1] if r+1 in range(shape[1]) and c+1 in range(shape[0]) else None,
                    grid[r+2][c  ] if r+2 in range(shape[1])                            else None,
                } - {None,}
                legals = set(string.ascii_lowercase) - conflicts
                if grid[r][c] in conflicts: grid[r][c] = random.choice(list(legals))
        return grid
   
class Letter(pg.sprite.Sprite):
    def __init__(self, letter, x, y, width, height):
        super().__init__()
        self.letter = letter
        pg.sprite.Sprite.__init__(self)
        font = ft.SysFont("Courier", 50)
        font.size = (width, height) # should probably check whether font is scalable
        (self.image, self.rect) = font.render(letter, fgcolor=FONT_COLOR)
        self.rect.topleft = (x, y) # how to position them well???

class Player(pg.sprite.Sprite):
    def __init__(self, grid_x, grid_y, stage):
        super().__init__()
        (width, height) = (stage.letter_width * 1, stage.letter_height * 1)
        self.image = pg.Surface((width, height))
        self.image.fill(PLAYER_COLOR)
        self.grid_pos = [grid_x, grid_y]
        abs_x = grid_x * stage.letter_width + stage.rect.left
        abs_y = grid_y * stage.letter_height + stage.rect.top
        self.rect = pg.Rect(abs_x, abs_y, width, height) # everything based on top left corner
        self.wpm_calc = WpmCalculator()
        self.curr_wpm = 0
    def move(self, text, stage):
        (r, c) = self.grid_pos # i don't know if this is x,y or y,x
        (w, h) = stage.grid_shape
        neighbor_offsets = {(-1,0), (0,-1), (0,1), (1,0)}
        neighbors = {
            stage.letters[r+os[0]][c+os[1]].letter: os
            for os in neighbor_offsets
            if (r+os[0] in range(h) and c+os[1] in range(w))
        }
        d_pos = neighbors.get(text)
        print(f"neighbors: {neighbors}, d_pos: {d_pos}")
        if d_pos is not None:
            self.wpm_calc.key()
            self.grid_pos[0] += d_pos[0] 
            self.grid_pos[1] += d_pos[1]
        lw, lh = stage.letter_width, stage.letter_height
        self.rect.left = self.grid_pos[0] * lw + stage.rect.left
        self.rect.top = self.grid_pos[1] * lh + stage.rect.top
        self.curr_wpm = self.wpm_calc.wpm()
        
class WpmCalculator():
    def __init__(self, historylen=20): # kinda shitty!
        self.delta_history = deque([1], maxlen=historylen)
        self.t0 = pg.time.get_ticks()
    def key(self):
        self.delta_history.append(pg.time.get_ticks() - self.t0)
        self.t0 = pg.time.get_ticks()
    def wpm(self):
        average = statistics.fmean(self.delta_history)
        word_length = 5
        return 1 / (average / 1000 / 60) / 5

def hud(player):
    return ft.SysFont("Courier", 18).render(f"WPM: {player.curr_wpm}")

stage = Stage()
stage_group = pg.sprite.GroupSingle(stage)
letters_group = pg.sprite.Group()
for row in stage.letters:
    for spr in row:
        letters_group.add(spr)
player1 = Player(0, 0, stage)
players_group = pg.sprite.Group()
players_group.add(player1)

def update():
    stage_group.update()
    players_group.update()
    letters_group.update()

def render():
    screen.fill(BG_COLOR)
    stage_group.draw(screen)
    players_group.draw(screen)
    letters_group.draw(screen)
    screen.blit(*hud(player1))
    pg.display.flip()

clock = pg.time.Clock()
pg.key.start_text_input() # this stays here until I have a menu screen 
while True:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        # should I use text input? how should I organize the call??
        elif event.type == pg.TEXTINPUT:
            player1.move(event.text, stage) # hmm, is this the most general way to do things
    update() # idt ths s effcient / a gd wy to cmprtmntlze
    render()
