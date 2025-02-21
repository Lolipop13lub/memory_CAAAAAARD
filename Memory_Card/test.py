from tkinter import *
w = Tk()

b = Button()

b.config(command=lambda: b.config(bg="red"))

b.pack()
w.mainloop()