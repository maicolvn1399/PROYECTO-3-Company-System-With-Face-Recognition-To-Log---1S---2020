import tkinter as tk
import tkinter.filedialog
import sys
import shutil
import os
import sys
import sqlite3#necesario para manejar la base de datos
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from new_user_class import NewUser
from face_recognition_class import FaceRecognition
from invoices_interface import InvoicesInterface
from add_user_class import RegisterUserInterface
from C3ProyectServicios import Servicio



#-------Menu Principal----------------------------------------------------------------------------------------
"""padx, pady : cuántos píxeles para rellenar el widget, horizontal y verticalmente, fuera de los bordes del objeto.
"""
class Window2:
    def __init__(self,master):
        #Atributos
        self.master = master
        self.master.geometry("400x400+300+300")
        self.master.title("Face Recognition App")
        self.label1 = tk.Label(self.master,text = "Facial Recognition App",font=("helvetica",19)).grid()
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame,text = "Services",width = 25,command = self.new_window).grid(padx=100, pady=10 , sticky=E+W)
        self.quitButton = tk.Button(self.frame,text = "Invoices",width = 25,command = self.new_window1).grid(padx=100, pady=10, sticky=E+W)
        self.loginButton = tk.Button(self.frame,text = "Login",width = 25,command = self.new_window2).grid(padx=100, pady=10, sticky=E+W)
        self.registerUser = tk.Button(self.frame,text = "Register User",width = 25,command = self.new_window3).grid(padx=100, pady=10, sticky=E+W)
        self.quitButton = tk.Button(self.frame,text = "QUIT",width = 25,command = self.close_windows).grid(padx=100, pady=10 , sticky=E+W )
        self.frame.grid()

        #metodos estos crean las diferentes ventanas o la destruyen.
    def close_windows(self):
        self.master.destroy()

    def new_window(self):
        self.new_window = Tk()
        self.app = Servicio(self.new_window)
        
    def new_window1(self):
        self.new_window_invoices = Tk()
        self.app1 = InvoicesInterface(self.new_window_invoices)#en vez de window2 va el nombre de la clase

    def new_window2(self):
        self.face_recognition_start = FaceRecognition()
        self.face_recognition_start.Recognize()

    def new_window3(self):
        self.register = RegisterUserInterface()




#----Clase Servicios------------------------------------------------------------------------------------------
class Servicio:
    # nombre de la base de datos
    db_name = 'database.db'

    def __init__(self, window):
        # Inicializacion 
        self.wind = window
        self.wind.title('3C: Company System With Face Recognition To Log')

        # Crea frame para posicionar la creacion de servicio 
        frame = LabelFrame(self.wind, text = 'Registrar Nuevo Servicio')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # input de nombre del nuevo servicio
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # input del precio del servicio
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Guarda los datos del nuevo servicio
        ttk.Button(frame, text = 'Guardar', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # configuacion de mensajes
        self.message = Label(self.wind,text = '', fg = 'green')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Tabla donde se muestran los datos
        #se crea la tabla y se define la ubicacion y e tamaño

        self.treeview = ttk.Treeview(self.wind,height = 10, columns = 2)
        self.treeview.grid(row = 4, column = 0, columnspan = 2)
        self.treeview.heading('#0', text = 'Nombre', anchor = CENTER)
        self.treeview.heading('#1', text = 'Precio', anchor = CENTER)

        # botones con sus respectivas funcionalidades
        self.button1 = ttk.Button(self.wind,text = 'ELIMINAR', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        self.button1 = ttk.Button(self.wind,text = 'EDITAR', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E,)

        # actualiza los datos
        self.get_products()

    # accede a la base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:#ingresa a la base de datos
            cursor = conn.cursor()#encuentr posicion
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # obtiene los servicios de la base de datos
    def get_products(self):
        # limpia la tabla 
        self.records = self.treeview.get_children()
        for element in self.records:
            self.treeview.delete(element)
        # actualiza los datos
        query = 'SELECT * FROM product ORDER BY name DESC'#muestra la tabla de la base de datos
        db_rows = self.run_query(query)
        # posiciona cada dato en la tabla
        for row in db_rows:
            self.treeview.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    #agregar servicio de la base de datos
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'#agrega servicio a la base de datos y crea un ID unico para este
            parameters =  (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = ' {} Fue agregado Satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Digite el nombre y el precio'
        self.get_products()
    #elimina servicio de la base de datos
    def delete_product(self):
        self.message['text'] = ''
        try:
           self.treeview .item(self.treeview.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione un servicio por favor'
            return
        self.message['text'] = ''
        name = self.treeview .item(self.treeview.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'#elimina el servicio de la base de datos
        self.run_query(query, (name, ))
        self.message['text'] = '  {} fue eliminado Satisfactoriamente'.format(name)
        self.get_products()
    #actualiza el servicio
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.treeview .item(self.treeview .selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione un servicio por favor'
            return
        name = self.treeview .item(self.treeview.selection())['text']#selecciona servicio de la  tabla
        old_price = self.treeview .item(self.treeview.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Servicio'
        # nombre del servicio
        Label(self.edit_wind, text = 'Nombre:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # nuevo nombre del servicio
        Label(self.edit_wind, text = 'Nuevo Nombre:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Precio del servicio 
        Label(self.edit_wind, text = 'Precio:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        #Nuevo precio del servico
        Label(self.edit_wind, text = 'Precio Nuevo:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)
        #ejecuta la funcion edit-records
        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()
        #Actualiza los cambios
    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'#actualiza los datos de la base de datos
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = '  {} fue actualizado satisfactoriamente'.format(name)
        self.get_products()
        

#-------------------------------------------------------------------------------------------------------------

def main():
    root = tk.Tk()
    app = Window2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
