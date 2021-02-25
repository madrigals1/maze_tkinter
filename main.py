import random
import sys
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

import constants
from constants import T


class MainFrame:
    def __init__(self, master):
        # Settings
        self.width_of_window = constants.WINDOW_WIDTH
        self.height_of_window = constants.WINDOW_HEIGHT
        self.maze_width = 0
        self.maze_height = 0
        self.block_height = 0
        self.canvas = None
        self.zero_amount = 0
        self.cur_x = 1
        self.cur_y = 1
        self.direction = 0
        self.path_list = []
        self.elem_list = []
        self.solution_show = True
        self.main_title = T.MAZE

        self.master = master
        master.title(self.main_title)
        master.bind("<KeyPress>", self.press)

        self.center()

        self.main_panel = PanedWindow(master, orient=VERTICAL)
        self.main_panel.pack()
        self.main_panel.place(rely=0.5, relx=0.5, anchor="center")
        self.my_font = Font(family=constants.FONT, size=15)
        self.label = Label(master, text=T.MAIN_TEXT, font=self.my_font)
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

        self.t_btn = Button(text=T.SHOW_SOLUTION, width=12, command=self.toggle)
        self.t_btn.pack(pady=5)

        self.button = Button(
            master, text=T.GENERATE, command=self.generate, font=self.my_font
        )

        self.main_panel.add(self.x_panel)
        self.main_panel.add(self.y_panel)
        self.main_panel.add(self.t_btn)
        self.main_panel.add(self.button)

    def toggle(self):
        self.solution_show = not self.solution_show
        text = T.SHOW_SOLUTION if self.solution_show else T.DONT_SHOW_SOLUTION
        self.t_btn.config(text=text)

    def press(self, e):
        if e.keysym == "Escape":
            self.restart()
        if e.keysym == "Return":
            self.generate()

    def restart(self):
        self.canvas and self.canvas.destroy()
        self.__init__(self.master)

    def center(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_coordinate = (screen_width / 2) - (self.width_of_window / 2)
        y_coordinate = (screen_height / 2) - (self.height_of_window / 2)

        self.master.geometry(
            "%dx%d+%d+%d"
            % (self.width_of_window, self.height_of_window, x_coordinate, y_coordinate)
        )

    def generate(self):
        if (
            int(self.x_entry.get()) <= 1
            or int(self.x_entry.get()) > 128
            or int(self.x_entry.get()) <= 1
            or int(self.x_entry.get()) > 128
        ):
            messagebox.showerror("Error", T.ALLOWED_SIZE_LIMIT)
        else:
            self.maze_width = int(self.x_entry.get()) * 2 + 1
            self.maze_height = int(self.y_entry.get()) * 2 + 1

            self.main_panel.destroy()

            self.block_height = int(
                (self.master.winfo_screenheight() - 150) / self.maze_height
            )
            self.width_of_window = self.block_height * self.maze_width
            self.height_of_window = self.block_height * self.maze_height

            self.can = Canvas(
                self.master,
                width=self.master.winfo_screenwidth(),
                height=self.master.winfo_screenheight(),
            )
            self.can.pack(expand=YES, fill=BOTH)

            self.center()

            for i in range(0, self.maze_width):
                self.elem_list.append([])
                for j in range(0, self.maze_height):
                    if (
                        i in [0, self.maze_width - 1]
                        or j in [0, self.maze_height - 1]
                        or i % 2 == 0
                        or j % 2 == 0
                    ):
                        self.elem_list[i].append(1)
                    else:
                        self.elem_list[i].append(0)

            self.zero_amount = int(self.x_entry.get()) * int(self.y_entry.get())
            self.find_path()
            self.elem_list[self.maze_height - 2][self.maze_width - 2] = 4

            if self.solution_show:
                self.solution(1, 1)
            else:
                self.draw_labyrinth()

    def solution(self, x, y):
        maze = self.elem_list
        if (
            x in [0, self.maze_height]
            or y in [0, self.maze_width]
            or maze[x][y] in [1, 5]
        ):
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
                args = [
                    i * self.block_height,
                    j * self.block_height,
                    (i + 1) * self.block_height,
                    (j + 1) * self.block_height,
                ]
                kwargs = {}
                if self.elem_list[i][j] == 1:
                    kwargs["fill"] = constants.WALL_COLOR
                elif self.elem_list[i][j] == 5:
                    kwargs["fill"] = constants.PATH_COLOR
                else:
                    kwargs["fill"] = constants.EMPTY_COLOR
                    kwargs["outline"] = constants.EMPTY_COLOR
                self.can.create_rectangle(*args, **kwargs)

    def find_path(self):
        self.elem_list[self.cur_x][self.cur_y] = 2
        self.zero_amount -= 1
        while self.zero_amount > 0:
            possible_list = self.check_valid()
            if len(possible_list):
                self.direction = random.choice(possible_list)
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

        if self.cur_x + 1 != self.maze_width - 1:
            if (
                self.elem_list[self.cur_x + 1][self.cur_y] != 3
                and self.elem_list[self.cur_x + 2][self.cur_y] != 2
            ):
                temp_list.append(0)

        if self.cur_y + 1 != self.maze_height - 1:
            if (
                self.elem_list[self.cur_x][self.cur_y + 1] != 3
                and self.elem_list[self.cur_x][self.cur_y + 2] != 2
            ):
                temp_list.append(1)

        if self.cur_x - 1 != 0:
            if (
                self.elem_list[self.cur_x - 1][self.cur_y] != 3
                and self.elem_list[self.cur_x - 2][self.cur_y] != 2
            ):
                temp_list.append(2)

        if self.cur_y - 1 != 0:
            if (
                self.elem_list[self.cur_x][self.cur_y - 1] != 3
                and self.elem_list[self.cur_x][self.cur_y - 2] != 2
            ):
                temp_list.append(3)

        return temp_list

    def set_path(self):
        if self.direction == 0:
            self.elem_list[self.cur_x + 1][self.cur_y] = 3
            self.elem_list[self.cur_x + 2][self.cur_y] = 2
            self.cur_x += 2
        if self.direction == 1:
            self.elem_list[self.cur_x][self.cur_y + 1] = 3
            self.elem_list[self.cur_x][self.cur_y + 2] = 2
            self.cur_y += 2
        if self.direction == 2:
            self.elem_list[self.cur_x - 1][self.cur_y] = 3
            self.elem_list[self.cur_x - 2][self.cur_y] = 2
            self.cur_x -= 2
        if self.direction == 3:
            self.elem_list[self.cur_x][self.cur_y - 1] = 3
            self.elem_list[self.cur_x][self.cur_y - 2] = 2
            self.cur_y -= 2

    def redefine(self):
        for i in range(0, self.maze_width):
            for j in range(0, self.maze_height):
                if self.elem_list[i][j] == 2 or self.elem_list[i][j] == 3:
                    self.elem_list[i][j] = 0


sys.setrecursionlimit(constants.RECURSION_LIMIT)
root = Tk()
gui = MainFrame(root)

root.mainloop()
