from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import random
import sys


class MainFrame:
    width_of_window = 500
    height_of_window = 500
    maze_width = 0
    maze_height = 0
    block_height = 0
    can = None
    zero_amount = 0
    cur_x = 1
    cur_y = 1
    dir = 0
    path_list = []
    elem_list = []

    def down(self, e):
        if e.keysym == 'Escape':
            self.restart()
        if e.keysym == 'Return':
            self.generate()

    def restart(self):
        if self.can:
            self.can.destroy()
        self.__init__(self.master)

    def __init__(self, master):
        self.master = master
        master.title("Maze Generator")
        master.bind('<KeyPress>', self.down)

        self.width_of_window = 500
        self.height_of_window = 500
        self.width_of_window = 500
        self.height_of_window = 500
        self.maze_width = 0
        self.maze_height = 0
        self.block_height = 0
        self.can = None
        self.zero_amount = 0
        self.cur_x = 1
        self.cur_y = 1
        self.dir = 0
        self.path_list = []
        self.elem_list = []

        self.center()

        self.main_panel = PanedWindow(master, orient=VERTICAL)
        self.main_panel.pack()
        self.main_panel.place(rely=0.5, relx=0.5, anchor='center')
        self.my_font = Font(family="Times New Roman", size=15)
        self.label = Label(master, text="Choose size of the labyrinth", font=self.my_font)
        self.main_panel.add(self.label)

        self.x_panel = PanedWindow(master, orient=HORIZONTAL)
        self.x_label = Label(master, text="Width :\t", font=self.my_font)
        self.x_entry = Entry(master, font=self.my_font)
        self.x_panel.add(self.x_label)
        self.x_panel.add(self.x_entry)

        self.y_panel = PanedWindow(master, orient=HORIZONTAL)
        self.y_label = Label(master, text="Height :\t", font=self.my_font)
        self.y_entry = Entry(master, font=self.my_font)
        self.y_panel.add(self.y_label)
        self.y_panel.add(self.y_entry)

        self.x_entry.focus()

        self.button = Button(master, text="Generate", command=self.generate, font=self.my_font)

        self.main_panel.add(self.x_panel)
        self.main_panel.add(self.y_panel)
        self.main_panel.add(self.button)

    def center(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_coordinate = (screen_width / 2) - (self.width_of_window / 2)
        y_coordinate = (screen_height / 2) - (self.height_of_window / 2)

        self.master.geometry("%dx%d+%d+%d" % (self.width_of_window, self.height_of_window, x_coordinate, y_coordinate))

    def generate(self):
        if int(self.x_entry.get()) <= 1 or int(self.x_entry.get()) > 128 or int(self.x_entry.get()) <= 1 or int(
                self.x_entry.get()) > 128:
            messagebox.showerror("Error", "Allowed size of Labyrinth is from 2x2 to 128x128")
        else:
            self.maze_width = int(self.x_entry.get()) * 2 + 1
            self.maze_height = int(self.y_entry.get()) * 2 + 1

            self.main_panel.destroy()

            self.block_height = int((self.master.winfo_screenheight() - 150) / self.maze_height)
            self.width_of_window = self.block_height * self.maze_width
            self.height_of_window = self.block_height * self.maze_height

            self.can = Canvas(self.master, width=self.master.winfo_screenwidth(),
                              height=self.master.winfo_screenheight())
            self.can.pack(expand=YES, fill=BOTH)

            self.center()

            for i in range(0, self.maze_width):
                self.elem_list.append([])
                for j in range(0, self.maze_height):
                    if i == 0 or j == 0 or i == self.maze_width - 1 or j == self.maze_height - 1:
                        self.elem_list[i].append(1)
                    elif i % 2 == 0 or j % 2 == 0:
                        self.elem_list[i].append(1)
                    else:
                        self.elem_list[i].append(0)

            self.zero_amount = int(self.x_entry.get()) * int(self.y_entry.get())
            self.find_path()
            self.elem_list[self.maze_height - 2][self.maze_width - 2] = 4

            self.solution(1, 1)

    def solution(self, x, y):
        maze = self.elem_list
        if x == 0 or x == self.maze_height or y == 0 or y == self.maze_width or maze[x][y] == 1 or maze[x][y] == 5:
            return 0
        if maze[x][y] == 4:
            maze[x][y] = 5
            self.draw_labyrinth()
            maze[x][y] = 4
            return 1

        t = maze[x][y]
        maze[x][y] = 5
        self.solution(x + 1, y)
        self.solution(x - 1, y)
        self.solution(x, y + 1)
        self.solution(x, y - 1)
        maze[x][y] = t

        return 0

    def draw_labyrinth(self):
        for i in range(0, self.maze_width):
            for j in range(0, self.maze_height):
                if self.elem_list[i][j] == 1:
                    self.can.create_rectangle(i * self.block_height, j * self.block_height,
                                              (i + 1) * self.block_height,
                                              (j + 1) * self.block_height, fill='black')
                elif self.elem_list[i][j] == 5:
                    self.can.create_rectangle(i * self.block_height, j * self.block_height,
                                              (i + 1) * self.block_height,
                                              (j + 1) * self.block_height, fill='green')
                else:
                    self.can.create_rectangle(i * self.block_height, j * self.block_height,
                                              (i + 1) * self.block_height,
                                              (j + 1) * self.block_height, fill="#ddd", outline="#ddd")

    def print_labyrinth(self):
        for i in range(0, self.maze_width):
            s = ""
            for j in range(0, self.maze_height):
                s += str(self.elem_list[i][j]) + " "
            print(s)

    def find_path(self):
        self.elem_list[self.cur_x][self.cur_y] = 2
        self.zero_amount -= 1
        while self.zero_amount > 0:
            possible_list = self.check_valid()
            if len(possible_list):
                self.dir = random.choice(possible_list)
                if len(possible_list) > 1:
                    self.path_list.append([self.cur_x, self.cur_y])
                self.set_path()
                self.zero_amount -= 1
            else:
                path = random.choice(self.path_list)
                self.path_list.remove(path)
                self.cur_x = path[0]
                self.cur_y = path[1]

    def check_valid(self):
        temp_list = []

        if self.cur_x + 1 is not self.maze_width - 1:
            if self.elem_list[self.cur_x + 1][self.cur_y] is not 3 and \
                    self.elem_list[self.cur_x + 2][self.cur_y] is not 2:
                temp_list.append(0)

        if self.cur_y + 1 is not self.maze_height - 1:
            if self.elem_list[self.cur_x][self.cur_y + 1] is not 3 and \
                    self.elem_list[self.cur_x][self.cur_y + 2] is not 2:
                temp_list.append(1)

        if self.cur_x - 1 is not 0:
            if self.elem_list[self.cur_x - 1][self.cur_y] is not 3 and \
                    self.elem_list[self.cur_x - 2][self.cur_y] is not 2:
                temp_list.append(2)

        if self.cur_y - 1 is not 0:
            if self.elem_list[self.cur_x][self.cur_y - 1] is not 3 and \
                    self.elem_list[self.cur_x][self.cur_y - 2] is not 2:
                temp_list.append(3)

        return temp_list

    def set_path(self):
        if self.dir == 0:
            self.elem_list[self.cur_x + 1][self.cur_y] = 3
            self.elem_list[self.cur_x + 2][self.cur_y] = 2
            self.cur_x += 2
        if self.dir == 1:
            self.elem_list[self.cur_x][self.cur_y + 1] = 3
            self.elem_list[self.cur_x][self.cur_y + 2] = 2
            self.cur_y += 2
        if self.dir == 2:
            self.elem_list[self.cur_x - 1][self.cur_y] = 3
            self.elem_list[self.cur_x - 2][self.cur_y] = 2
            self.cur_x -= 2
        if self.dir == 3:
            self.elem_list[self.cur_x][self.cur_y - 1] = 3
            self.elem_list[self.cur_x][self.cur_y - 2] = 2
            self.cur_y -= 2

    def redefine(self):
        for i in range(0, self.maze_width):
            for j in range(0, self.maze_height):
                if self.elem_list[i][j] == 2 or self.elem_list[i][j] == 3:
                    self.elem_list[i][j] = 0


sys.setrecursionlimit(2000)
root = Tk()
gui = MainFrame(root)

root.mainloop()


