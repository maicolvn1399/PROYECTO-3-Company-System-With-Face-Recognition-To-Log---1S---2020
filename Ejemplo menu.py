import tkinter as tk                
from tkinter import font  as tkfont 
from tkinter import ttk
from tkinter import *
import sqlite3

class C3App(tk.Tk):
    
    

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Franklin Gothic Book', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=19)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Facturas, Servicios, Informe):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
##        frame.config(bg="LightBlue")
        frame.config(width=480,height=320) 
        frame.tkraise()

        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        label = tk.Label(self, text="3C: Company System ", font=controller.title_font)
        label.pack(pady=20)

        button1 = tk.Button(self, text="Facturas",
                            command=lambda: controller.show_frame("Facturas")).pack()
        button2 = tk.Button(self, text="Servicios",
                            command=lambda: controller.show_frame("Servicios")).pack()
        button3 = tk.Button(self, text="Informe General",
                            command=lambda: controller.show_frame("Informe")).pack()
        
class Facturas(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Facturacion", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        button = tk.Button(self, text="Volver al menu principal",
                           command=lambda: controller.show_frame("StartPage")).pack( pady=100)
        

class Servicios(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Servicios", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        button = tk.Button(self, text="Volver al menu principal",
                           command=lambda: controller.show_frame("StartPage")).pack(pady=100)
       
        
class Informe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Informe General", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        button = tk.Button(self, text="volver al menu principal",
                           command=lambda: controller.show_frame("StartPage")).pack(pady=100)
        

if __name__ == "__main__":

    app = C3App()
    app.geometry("400x300")
    app.title("3C: Company System With Face Recognition To Log")
    app.mainloop()
