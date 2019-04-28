from tkinter import *
from tkinter.font import Font


class MainFrame:
	width_of_window = 500
	height_of_window = 500
	mazeWidth = 0
	mazeHeight = 0

	def __init__(self, master):
		self.master = master
		master.title("Maze Generator")

		self.center()

		self.mainPanel = PanedWindow(master, orient=VERTICAL)
		self.mainPanel.pack()
		self.mainPanel.place(rely=0.5, relx=0.5, anchor='center')
		self.myfont = Font(family="Times New Roman", size=15)
		self.label = Label(master, text="Choose size of the labyrinth", font=self.myfont)
		self.mainPanel.add(self.label)

		self.xPanel = PanedWindow(master, orient=HORIZONTAL)
		self.xlabel = Label(master, text="Width :\t", font=self.myfont)
		self.xentry = Entry(master, font=self.myfont)
		self.xPanel.add(self.xlabel)
		self.xPanel.add(self.xentry)

		self.yPanel = PanedWindow(master, orient=HORIZONTAL)
		self.ylabel = Label(master, text="Height :\t", font=self.myfont)
		self.yentry = Entry(master, font=self.myfont)
		self.yPanel.add(self.ylabel)
		self.yPanel.add(self.yentry)

		self.xentry.focus()

		self.button = Button(master, text="Generate", command=self.generate, font=self.myfont)

		self.mainPanel.add(self.xPanel)
		self.mainPanel.add(self.yPanel)
		self.mainPanel.add(self.button)

	def center(self):
		screen_width = self.master.winfo_screenwidth()
		screen_height = self.master.winfo_screenheight()

		x_coordinate = (screen_width / 2) - (self.width_of_window / 2)
		y_coordinate = (screen_height / 2) - (self.height_of_window / 2)

		self.master.geometry("%dx%d+%d+%d" % (self.width_of_window, self.height_of_window, x_coordinate, y_coordinate))

	def generate(self):
		self.mazeWidth = int(self.xentry.get()) * 2 + 1
		self.mazeHeight = int(self.yentry.get()) * 2 + 1

		self.mainPanel.destroy()

		blockHeight = int((self.master.winfo_screenheight() - 150) / self.mazeHeight)
		self.width_of_window = blockHeight * self.mazeWidth
		self.height_of_window = blockHeight * self.mazeHeight

		self.canvas = Canvas(self.master, width=self.master.winfo_screenwidth(), height=self.master.winfo_screenheight())
		self.canvas.pack(expand=YES, fill=BOTH)
		
		self.center()

		for i in range(0, self.mazeWidth):
			for j in range(0, self.mazeHeight):
				if i == 0 or j == 0 or i == self.mazeWidth - 1 or j == self.mazeHeight - 1:
					self.canvas.create_rectangle(i * blockHeight, j * blockHeight, (i + 1) * blockHeight, (j + 1) * blockHeight, fill='black')
				else:
					self.canvas.create_rectangle(i * blockHeight, j * blockHeight, (i + 1) * blockHeight,
												 (j + 1) * blockHeight, outline="#fb0", fill="#ddd")




class MazeFrame:
	def __init__(self, master):
		self.master = master
		master.title = "Second Page"


root = Tk()
gui = MainFrame(root)

root.mainloop()
