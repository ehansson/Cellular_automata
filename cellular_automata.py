# -*- coding: utf-8 -*-
"""
Cellular automata
Created on Fri Jan 19 18:40:04 2024

@author: ehansson
"""

import tkinter as tk
import random
from binaryconverter import dec2binarylist
from PIL import ImageGrab
import tkinter.filedialog as filedialog

GRID = 5
SCREENWIDTH = GRID*200
SCREENHEIGHT = GRID*120
SCREENCOLOR = "#888888"
ONCOLOR = "#FFFFFF"
OFFCOLOR = "#202020"
zoom = 1.25 #My computer has 125% screensize by default, adjust to fit your own
            #On Windows 10 it is under Settings->Display->Scale and Layout


class Cell:
    def __init__(self, canvas, col_idx, row_idx):
        self.coords = [col_idx*GRID, row_idx*GRID]
        self.state = 0
        self.canvas = canvas
        
        x, y = self.coords
        self.cell = self.canvas.create_rectangle(x, y, x+GRID, y+GRID, 
                                         fill=OFFCOLOR, tag="cell")
        
    def change(self):
        self.state = (self.state + 1)%2
        if self.state == 0:
            color = OFFCOLOR
        if self.state == 1:
            color = ONCOLOR
        self.canvas.itemconfig(self.cell, fill=color)
        
    def reset(self):
        self.state = 0
        self.canvas.itemconfig(self.cell, fill=OFFCOLOR)
        
        
class Rows:
    def __init__(self, canvas, firstrow):
        self.canvas = canvas
        self.length = len(firstrow)
        self.height = SCREENHEIGHT
        self.row_idx = 0
        self.cells = []
        self.states = firstrow
        self.rules = {(1,1,1) : 0, (1,1,0) : 0,
                      (1,0,1) : 0, (1,0,0) : 0,
                      (0,1,1) : 0, (0,1,0) : 0,
                      (0,0,1) : 0, (0,0,0) : 0}

        
        #Draw all cells
        for row in range(int(SCREENHEIGHT/GRID)):
            for idx in range(int(SCREENWIDTH/GRID)):
                self.cells.append(Cell(self.canvas, idx, row))
        
        for idx in range(self.length):
            if self.states[idx] == 1:
                self.cells[idx].change()

        
    def draw(self, changes):
        for x in changes:
            self.cells[x + self.row_idx*self.length].change()
           
            
    def next_row(self, newrules):
        
        i = 0
        for rule in self.rules:
            self.rules[rule] = newrules[i]
            i += 1
           
        self.row_idx += 1
        next_states = []
        changes = []
        for idx in range(self.length):
            left_neighbour = self.states[idx-1]
            right_neighbour = self.states[(idx+1)%self.length]
            next_states.insert(idx, self.rules[
                (left_neighbour, self.states[idx], right_neighbour)])
            if next_states[idx] == 1:
                changes.append(idx)
        self.states = next_states
        self.draw(changes)
        
class Plane:
    def __init__(self, canvas, firstplane):
        self.canvas = canvas
        self.height = len(firstplane)
        self.width = len(firstplane[0])
        self.cells = [[0 for w in range(self.width)] for h in range(self.height)]
        self.states = firstplane
        self.changes = []
        
        for h in range(self.height):
            for w in range(self.width):
                self.cells[h][w] = (Cell(self.canvas, w, h))
                if self.states[h][w] == 1:
                    self.changes.append((h,w))
                
        self.draw()
        
    def turn_on(self, cell):
        self.canvas.itemconfig(cell.cell, fill=ONCOLOR)
                
    def turn_off(self, cell):
        self.canvas.itemconfig(cell.cell, fill=OFFCOLOR)
                
    def next_generation(self):
        next_states = [[0 for w in range(self.width)] for h in range(self.height)]
        
        for h in range(self.height):
            for w in range(self.width):
                #UL, U, UR
                #L,  C,  R
                #DL, D, DR
                UL = self.states[(h-1)%self.height][(w-1)%self.width]
                U = self.states[(h-1)%self.height][w]
                UR = self.states[(h-1)%self.height][(w+1)%self.width]
                L = self.states[h][(w-1)%self.width]
                C = self.states[h][w]
                R = self.states[h][(w+1)%self.width]
                DL = self.states[(h+1)%self.height][(w-1)%self.width]
                D = self.states[(h+1)%self.height][w]
                DR = self.states[(h+1)%self.height][(w+1)%self.width]
                
                neigbours = [UL, U, UR, L, R, DL, D, DR]
                
                #Rules for Game of Life
                if C == 0 and sum(neigbours) == 3: #If exactly 3 neigbours cell is born
                        next_states[h][w] = 1
                        self.changes.append((h,w))
                
                elif C == 1 and sum(neigbours) not in [2,3]:
                        next_states[h][w] = 0 #If not 2 or 3 neighbors, cell dies
                        self.changes.append((h,w))
                else: 
                    next_states[h][w] = C
                    
        self.states = next_states
        
    
    def draw(self):
        for y, x in self.changes:
            self.cells[y][x].change()
        self.changes = []


class CellularAutomaton1D(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.create_widgets()
        
    def create_widgets(self):
        self.rule = tk.IntVar()
        # Create "Run" button
        self.run_button = tk.Button(
            self, text="Run", command=self.run)
        self.run_button.grid(column=0, row=0)
        # Create "Quit" button
        self.quit_button = tk.Button(
            self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(column=0, row=1) #Crashes if command=self.quit
        # Create "Save" button
        self.save_button = tk.Button(
            self, text="Save", command=self.save_image)
        self.save_button.grid(column=3, row=0)
        # Create entry box for custom rule
        self.ruleEntry = tk.Entry(self)
        self.ruleEntry.grid(column=2, row=1)
        self.ruleEntry.insert(10, 106) #106 is default (because it looks cool)
        # Create radiobuttons for choosing beween random or custom rule
        self.rulechoice = tk.IntVar()
        self.rulechoice.set(0) #Random rule is default
        self.randRadiobutton = tk.Radiobutton(
            self, text="Random rule", variable=self.rulechoice, value=0)
        self.randRadiobutton.grid(column=1, row=0)
        self.customRadiobutton = tk.Radiobutton(
            self, text="Custom rule", variable=self.rulechoice, value=1)
        self.customRadiobutton.grid(column=1, row=1)
        # Create canvas for displacing evolution of cells
        self.canvas = tk.Canvas(
            self, width=SCREENWIDTH, height=SCREENHEIGHT, bg=SCREENCOLOR)
        self.canvas.grid(column=0, row=2, columnspan=4)
        self.create_cells()
        # Show current rule
        self.showrule = tk.Label(self, text = "Current rule: 0", compound=tk.LEFT)
        self.showrule.grid(column=2, row=0)
    
    def get_rules(self):
        if self.rulechoice.get() == 0:  #Random rule
            self.rule.set(random.randint(0, 255))
        elif self.rulechoice.get() == 1:
            try:  #Custom rule
                self.rule.set(int(self.ruleEntry.get()))
            except:
                self.rule.set(0)
                print('Enter a rule between 0 and 255 or choose "Random rule"')
        else:   #If for some reason a bug happens where none of the radiobuttons are selected
            self.rule.set(0)
            print('Choose "Random rule" or "Custom rule"')
        return self.rule.get()

        
    def create_cells(self):
        self.startingcells = [random.randint(0, 1) for x in range(int(SCREENWIDTH/GRID))]
        
        # Print cells
        self.rows = Rows(self.canvas, self.startingcells)
            
    def run(self):
        self.rows.row_idx = 0
        self.reset_canvas()
        rule = self.get_rules()
        rulelist = dec2binarylist(rule)
        for _ in range(int(SCREENHEIGHT/GRID)-1):
            self.rows.next_row(rulelist)
        self.showrule.config(text="Current rule: " + str(self.rule.get()))
        
    def reset_canvas(self):
        for cell in self.rows.cells[int(SCREENWIDTH/GRID):]:
            cell.reset()
        self.rows.states = self.startingcells
        
    def save_image(self):
        self.update()
        filelocation = filedialog.asksaveasfilename(defaultextension="png")
        x = (self.winfo_rootx() + self.canvas.winfo_x())*zoom
        y = (self.winfo_rooty() + self.canvas.winfo_y())*zoom
        width = self.canvas.winfo_width()*zoom
        height = self.canvas.winfo_height()*zoom
        self.img = ImageGrab.grab(bbox=(x,y,x+width,y+height),
                                  include_layered_windows=False, all_screens=False)
        self.img.save(filelocation)
        
class GameOfLife(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.is_running = False
        
        self.create_widgets()
        self.print_cells()
        
    def create_widgets(self):
        self.rule = tk.IntVar()
        # Create "Run" button
        self.run_button = tk.Button(
            self, text="Generate", command=self.generate)
        self.run_button.grid(column=0, row=0)
        # Create "Run" button
        self.run_button = tk.Button(
            self, text="Run", command=self.run)
        self.run_button.grid(column=1, row=0)
        # Create "Stop" button
        self.run_button = tk.Button(
            self, text="Stop", command=self.stop)
        self.run_button.grid(column=1, row=1)
        # Create "Quit" button
        self.quit_button = tk.Button(
            self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(column=0, row=1) #Crashes if command=self.quit
        # Create "Save" button
        self.save_button = tk.Button(
            self, text="Save", command=self.save_image)
        self.save_button.grid(column=3, row=0)
        # Create canvas for displacing evolution of cells
        self.canvas = tk.Canvas(
            self, width=SCREENWIDTH, height=SCREENHEIGHT, bg=SCREENCOLOR)
        self.canvas.grid(column=0, row=2, columnspan=4)

    def print_cells(self):
        startingcells = [[random.randint(0, 1) for x in range(int(SCREENWIDTH/GRID))] 
                         for y in range(int(SCREENHEIGHT/GRID))]
        self.cells = Plane(self.canvas, startingcells)
        
    def generate(self):
        self.cells.next_generation()
        self.cells.draw()
        print("Done")
        
    def run(self):
        self.is_running = True
        while self.is_running == True:
            self.cells.next_generation()
            self.cells.draw()
            self.canvas.update()
            
    def stop(self):
        self.is_running = False
        
    def save_image(self):
        self.update()
        filelocation = filedialog.asksaveasfilename(defaultextension="png")
        x = (self.winfo_rootx() + self.canvas.winfo_x())*zoom
        y = (self.winfo_rooty() + self.canvas.winfo_y())*zoom
        width = self.canvas.winfo_width()*zoom
        height = self.canvas.winfo_height()*zoom
        self.img = ImageGrab.grab(bbox=(x,y,x+width,y+height),
                                  include_layered_windows=False, all_screens=False)
        self.img.save(filelocation)
        
            
app = GameOfLife()
app.master.title("Game of Life")
app.mainloop()




