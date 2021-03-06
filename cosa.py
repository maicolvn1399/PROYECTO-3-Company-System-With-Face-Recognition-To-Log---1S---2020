import tkinter as tk

from tkinter import *
from tkinter import ttk
import sqlite3


class Window:
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x400+300+300")
        self.master.title("Face Recognition App")
        self.label1 = tk.Label(self.master,text = "C3 Proyect").grid(row = 0, column = 2 )
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame,text = "Login",width = 25).grid(row = 1, column = 2 )
        self.button2 = tk.Button(self.frame,text = "Register",width = 25,command=self.new_window).grid(row = 2, column = 2 )
        self.frame.grid()
        self.uploadedImage = False

    def new_window(self):
        self.new_window = tk.Tk()
        self.app = Window2(self.new_window)

        

class Window2:
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x400+300+300")
        self.master.title("Face Recognition App")
        self.label1 = tk.Label(self.master,text = "C3 Proyect").grid()
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame,text = "Servicios",width = 25,command = self.new_window).grid(padx=100, pady=10 , sticky=E+W)
        self.quitButton = tk.Button(self.frame,text = "Facturas",width = 25,command = self.close_windows).grid(padx=100, pady=10, sticky=E+W)
        self.quitButton = tk.Button(self.frame,text = "QUIT",width = 25,command = self.close_windows).grid(padx=100, pady=10 , sticky=E+W )
        self.frame.grid()

    def close_windows(self):
        self.master.destroy()
        
    def new_window(self):
        new_window = Tk()
        Servicio(new_window)

class Servicio:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('3C: Company System With Face Recognition To Log')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Registrar Nuevo Servicio')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Price Input
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Button Add Product 
        ttk.Button(frame, text = 'Guardar', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(self.wind,text = '', fg = 'green')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table

        self.treeview = ttk.Treeview(self.wind,height = 10, columns = 2)
        self.treeview.grid(row = 4, column = 0, columnspan = 2)
        self.treeview.heading('#0', text = 'Nombre', anchor = CENTER)
        self.treeview.heading('#1', text = 'Precio', anchor = CENTER)

        # Buttons
        self.button1 = ttk.Button(self.wind,text = 'ELIMINAR', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        self.button1 = ttk.Button(self.wind,text = 'EDITAR', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E,)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        self.records = self.treeview.get_children()
        for element in self.records:
            self.treeview.delete(element)
        # getting data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.treeview.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = ' {} Fue agregado Satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Digite el nombre y el precio'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.treeview .item(self.treeview.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione un servicio por favor'
            return
        self.message['text'] = ''
        name = self.treeview .item(self.treeview.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = '  {} fue eliminado Satisfactoriamente'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.treeview .item(self.treeview .selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione un servicio por favor'
            return
        name = self.treeview .item(self.treeview.selection())['text']
        old_price = self.treeview .item(self.treeview.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Servicio'
        # Old description
        Label(self.edit_wind, text = 'Nombre:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New description
        Label(self.edit_wind, text = 'Nuevo Nombre:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Price 
        Label(self.edit_wind, text = 'Precio:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'Precio Nuevo:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = '  {} fue actualizado satisfactoriamente'.format(name)
        self.get_products()

#-------------------------------------------------------------------------------------------------------------------------------
        
def main():
    root = tk.Tk()
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
