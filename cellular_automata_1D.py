# -*- coding: utf-8 -*-
"""
Cellular automata
Created on Fri Jan 19 18:40:04 2024

@author: ehansson
"""

import tkinter as tk
import random
from binaryconverter import dec2binarylist

GRID = 5
SCREENWIDTH = GRID*200
SCREENHEIGHT = GRID*150
SCREENCOLOR = "#888888"
ONCOLOR = "#FFFFFF"
OFFCOLOR = "#202020"


class Cell:
    def __init__(self, canvas, col_idx, row_idx, state):
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
    def __init__(self, canvas, firstrow, newrules):
        self.canvas = canvas
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
            self.cells.append(Cell(self.canvas, idx, self.row_idx, self.states[idx]))
            
    def next_row(self):
        self.row_idx += 1
        next_states = []
        for idx in range(self.length):
            left_neighbour = self.states[idx-1]
            right_neighbour = self.states[(idx+1)%self.length]
            next_states.insert(idx, self.rules[
                (left_neighbour, self.states[idx], right_neighbour)])
        
        self.states = next_states
        self.draw()
        

class CellularAutomata1D(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.create_widgets()
        
    def create_widgets(self):
        self.run_button = tk.Button(
            self, text="Run", command=self.run)
        self.run_button.grid(column=0, row=0)
        self.quit_button = tk.Button(
            self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(column=0, row=1) #Crashes if command=self.quit
        self.ruleEntry = tk.Entry(self)
        self.ruleEntry.grid(column=2, row=1)
        self.ruleEntry.insert(10, 106)
        self.rulechoice = tk.IntVar()
        self.rulechoice.set(0) #Random rule is default
        self.randRadiobutton = tk.Radiobutton(
            self, text="Random rule", variable=self.rulechoice, value=0)
        self.randRadiobutton.grid(column=1, row=0)
        self.customRadiobutton = tk.Radiobutton(
            self, text="Custom rule", variable=self.rulechoice, value=1)
        self.customRadiobutton.grid(column=1, row=1)
        self.canvas = tk.Canvas(
            self, width=SCREENWIDTH, height=SCREENHEIGHT, bg=SCREENCOLOR)
        self.canvas.grid(column=0, row=2, columnspan=3)

        
    def run(self):
        
        if self.rulechoice.get() == 0:
            self.rule = random.randint(0, 255) #Random rules
        elif self.rulechoice.get() == 1:
            try:
                self.rule = int(self.ruleEntry.get())
            except:
                self.rule = 0
                print('Enter a rule between 0 and 255 or choose "Random rule"')
        else:
            self.rule = 0
            print('Enter a rule between 0 and 255 or choose "Random rule"')
        startingcells = [random.randint(0, 1) for x in range(int(SCREENWIDTH/GRID))]
        #rule = random.randint(0, 255) #Random rules
        #rule = 90 #Coolest rule I found so far! 60 is also cool
        rules = dec2binarylist(self.rule)
        print(self.rule)
        cells = Row(self.canvas, startingcells, rules)

        for _ in range(200):
            cells.next_row()
            
app = CellularAutomata1D()
app.master.title("1D automata")
app.mainloop()

