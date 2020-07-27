import tkinter as tk
from tkinter import messagebox
import newUser
import os
import sys

class Window:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame,text = "NEW WINDOW",width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Window2(self.new_window)

class Window2:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame,text = "QUIT",width = 25,command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
