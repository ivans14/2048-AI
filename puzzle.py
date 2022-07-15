from tkinter import Frame, Label, CENTER
import time
import random
import logic
import constants as c

import expectimax as exp
import numpy as np

import minimax as minmax

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()
        time.sleep(0.05)

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT: exit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                self.check_game_end()
                
        elif key == c.KEY_SOLVE:
            
            self.end = False
            depth = 1
            legal_moves = {c.KEY_UP: logic.up,
                           c.KEY_DOWN: logic.down,
                           c.KEY_LEFT: logic.left,
                           c.KEY_RIGHT: logic.right}
            move, _ = exp.expectimax(self.matrix, legal_moves, depth=depth, end=self.end)
            while not self.end:
                ran=np.random.randint(0,100,1,dtype=int)
                print(move)
                print(ran)
                self.matrix, done = self.commands[move](self.matrix)
                if done:
                    if ran<90:
                        self.matrix = logic.add_two(self.matrix)
                    else:
                        self.matrix = logic.add_four(self.matrix)
                        
                    # record last move
                    del(ran)
                    self.update_grid_cells()
                    time.sleep(0.2)
                    move, _ = exp.expectimax(self.matrix, legal_moves, depth=depth, end=self.end)
            self.check_game_end()

        elif key == c.MINIMAX:
            while True :
                self.end = False
                depth = 1
                legal_moves = {c.KEY_UP: logic.up,
                            c.KEY_DOWN: logic.down,
                            c.KEY_LEFT: logic.left,
                            c.KEY_RIGHT: logic.right}
                child=minmax.getBestMove(self.matrix, legal_moves, depth=depth)
                self.matrix,done=minmax.move_to_best(self.matrix,child)
                ran=np.random.randint(0,100,1,dtype=int)
                if done:
                    if ran<90:
                        self.matrix = logic.add_two(self.matrix)
                    else:
                        self.matrix = logic.add_four(self.matrix)
                    del(ran)
                time.sleep(0.05)
                self.update_grid_cells()
                self.check_game_end()



    def check_game_end(self):
        if logic.game_state(self.matrix) == 'win':
            self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.end = True
        if logic.game_state(self.matrix) == 'lose':
            self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.end = True

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


if __name__ == '__main__':
    game_grid = GameGrid()