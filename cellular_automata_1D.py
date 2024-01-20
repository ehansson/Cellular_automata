# -*- coding: utf-8 -*-
"""
Cellular automata
Created on Fri Jan 19 18:40:04 2024

@author: ehansson
"""

import tkinter as tk
import random

GRID = 5
SCREENWIDTH = GRID*200
SCREENHEIGHT = GRID*300
SCREENCOLOR = "#888888"
ONCOLOR = "#FFFFFF"
OFFCOLOR = "#202020"


class Cell:
    def __init__(self, col_idx, row_idx, state):
        self.coords = [col_idx*GRID, row_idx*GRID]
        self.state = state
        
        if self.state == 0:
            color = OFFCOLOR
        if self.state == 1:
            color = ONCOLOR
        x, y = self.coords
        canvas.create_rectangle(x, y, x+GRID, y+GRID, 
                                         fill=color, tag="cell")
        
        
class Row:
    def __init__(self, firstrow, newrules):
        self.length = len(firstrow)
        self.row_idx = 0
        self.cells = []
        self.states = firstrow
        self.rules = {(1,1,1) : None, (1,1,0) : None,
                      (1,0,1) : None, (1,0,0) : None,
                      (0,1,1) : None, (0,1,0) : None,
                      (0,0,1) : None, (0,0,0) : None}
        i = 0
        for rule in self.rules:
            self.rules[rule] = newrules[i]
            i += 1
        
        self.draw()
        
    def draw(self):
        for idx in range(self.length):
            self.cells.append(Cell(idx, self.row_idx, self.states[idx]))
            
    def next_row(self):
        self.row_idx += 1
        
        for idx in range(self.length):
            left_neighbour = self.states[idx-1]
            right_neighbour = self.states[(idx+1)%self.length]
            self.states[idx] = self.rules[
                (left_neighbour, self.states[idx], right_neighbour)]
        
        self.draw()
        
        
screen = tk.Tk()
canvas = tk.Canvas(screen, width=SCREENWIDTH, height=SCREENHEIGHT, bg=SCREENCOLOR)
canvas.pack()

startingcells = [random.randint(0, 1) for x in range(int(SCREENWIDTH/GRID))]
rules = [random.randint(0, 1) for x in range(8)]
print(rules)

cells = Row(startingcells, rules)

for _ in range(200):
    cells.next_row()

screen.mainloop()

