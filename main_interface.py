import tkinter as tk
import tkinter.filedialog
import sys
import shutil
import os
import sys
import sqlite3 #necesario para manejar la base de datos
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from new_user_class import NewUser
from face_recognition_class import FaceRecognition
from invoices_interface import InvoicesInterface
from add_user_class import RegisterUserInterface
from C3ProyectServicios import Servicio

class MainInterface:
    def __init__(self,window):
        self.window = window
        self.window.title("Facial Recognition App")
        self.window.minsize(width=500,height=600)
        self.label1 = tk.Label(self.window, text="Facial Recognition App",font=("Helvetica", 16)).grid(row=0,column=0)
        #self.label1.place(x=150,y=0)
        self.label2 = tk.Label(self.window, text="Welcome",font=("Helvetica", 16)).grid(row=1,column=0)
        #self.label2.place(x=150,y=80)
        self.buttonLogin = tk.Button(self.window,text= "Login",font = ("Helvetica", 15),command = self.start_face_recognizer).grid(row=2,column=0)
        #self.buttonLogin.place(x=150,y=120)
        self.buttonAddUser = tk.Button(self.window,text= "Register User",font = ("Helvetica", 15),command = self.start_register_user).grid(row=3,column=0)
        #self.buttonAddUser.place(x=150,y=160)
        self.buttonServices = tk.Button(self.window,text= "Services",font = ("Helvetica", 15),command = self.start_services).grid(row=4,column=0)
        #self.buttonServices.place(x=150,y=200)
        self.buttonInvoices = tk.Button(self.window,text= "Invoices",font = ("Helvetica", 15),command = self.start_invoices).grid(row=5,column=0)

        #self.buttonInvoices.place(x=150,y=240)


    def start_invoices(self):
        self.window1 = Tk()
        application = InvoicesInterface(self.window1)
        self.window1.mainloop()

    def start_face_recognizer(self):
        face_recognizer = FaceRecognition()
        face_recognizer.Recognize()

    def start_register_user(self):
        newWindow = RegisterUserInterface()

    def start_services(self):
        window2 = Tk()
        application = Servicio(window2)
        window2.mainloop()






win = Tk()
a = MainInterface(win)
win.mainloop()



