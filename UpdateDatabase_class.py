from tkinter import ttk
from tkinter import *
from datetime import datetime, date,timedelta
from tkcalendar import Calendar,DateEntry
from C3ProyectServicios import Servicio
from invoice_class import Invoice
from email_class import SendEmail
from bank_class import GetBankInformation
from tkinter import messagebox
import os,shutil
import sqlite3

class Prueba:

    database = "prueba_database.db"

    def __init__(self):
        self.window = Tk()
        self.window.title("Prueba")
        self.window.minsize(width=300,height=300)
        self.entry1 = Entry(self.window)
        self.entry1.grid(row=0,column=0)
        self.entry2 = Entry(self.window)
        self.entry2.grid(row=1,column=0)
        Button(self.window,text="Save",command = self.add_data).grid(row=2,column=0)
        Button(self.window,text="Modify",command = self.modify_data).grid(row=3,column=0)
        self.window.mainloop()

    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result

    def add_data(self):
        first = self.entry1.get()
        second = self.entry2.get()
        query = "INSERT INTO prueba_database VALUES(NULL,?,?)"
        parameters =(first,second)
        self.run_query(query, parameters)

    def modify_data(self):
        query = "UPDATE prueba_database set salary = ?"
        parameters = (23,)
        self.run_query(query,parameters)


p = Prueba()
