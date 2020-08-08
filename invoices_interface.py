import sqlite3
from tkinter import ttk
from tkinter import *
from datetime import datetime, date,timedelta
from tkcalendar import Calendar,DateEntry
from C3ProyectServicios import Servicio
from invoice_class import Invoice
from tkinter import messagebox
import sqlite3

class InvoicesInterface:

    db_name = "invoices_database.db"

    db_services = 'database.db'

    def __init__(self,window):
        """Con sqlite"""
        self.windowInvoices = window
        self.windowInvoices.title("Invoices Window")

        # Creating a Frame Container
        frame = LabelFrame(self.windowInvoices, text="Create an invoice")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name imput
        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Address Input
        Label(frame, text="Address: ").grid(row=2, column=0)
        self.address = Entry(frame)
        self.address.grid(row=2, column=1)

        # ID input
        Label(frame, text="ID: ").grid(row=3, column=0)
        self.ID_ = Entry(frame)
        self.ID_.grid(row=3, column=1)

        # Email input
        Label(frame, text="Email: ").grid(row=4, column=0)
        self.email = Entry(frame)
        self.email.grid(row=4, column=1)

        # Date input
        Label(frame, text="Date: ").grid(row=5, column=0)
        self.date = DateEntry(frame, width=12, background='darkblue',
                              foreground='white', borderwidth=2,date_pattern='YYYY-MM-DD')
        self.date.grid(row=5, column=1)

        # Service input
        # ***** Change to a combobox ****

        Label(frame, text="Service").grid(row=6, column=0)
        n = StringVar()
        self.service = ttk.Combobox(frame)
        self.service["values"] = self.get_services()
        self.service.set(self.get_services()[0])
        self.service.grid(row=6, column=1)

        Label(frame,text="Discount Percentaje").grid(row=7,column=0)
        self.discount = Entry(frame)
        self.discount.grid(row=7,column=1)

        # Button create invoice
        Button(frame, text="Create Invoice",command=self.add_invoice).grid(row=8, columnspan=2,sticky=W+E)

        #Output messages
        self.message = Label(frame,text="",fg='red')
        self.message.grid(row=9,column=0,columnspan=2,sticky = W + E)

        self.tree = ttk.Treeview(height=10,columns=("#0","#1","#2","#3","#4","#5","#6","#7","#8","#9"))
        self.tree.grid(row=10,column=0,columnspan=3)
        self.tree.heading("#0",text ="Name",anchor=CENTER)
        self.tree.heading("#1",text="ID",anchor=CENTER)
        self.tree.heading("#2",text="Email",anchor=CENTER)
        self.tree.heading("#3",text="Date",anchor = CENTER)
        self.tree.heading("#4",text="Due Date",anchor=CENTER)
        self.tree.heading("#5",text="Service",anchor=CENTER)
        self.tree.heading("#6",text="Price",anchor=CENTER)
        self.tree.heading("#7",text="Discount",anchor=CENTER)

        #Buttons
        Button(text="DELETE",command = self.delete_invoice).grid(row=11,column=0,sticky=W+E)

        #Filling rows of table
        self.get_invoices()

    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result

    def run_query_services(self,query,parameters = ()):
        with sqlite3.connect(self.db_services) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_services(self):
        list = []
        # getting data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query_services(query)
        # filling data
        for row in db_rows:
            #print(row)
            itemNum, service, price = row
            list += [service + " - " + "₡" + str(price)]

        return list

    def get_invoices(self):
        #cleaning table everytime it runs
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #quering data
        query = 'SELECT * FROM invoices ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            #print(row)
            #print(row[2:5])
            self.tree.insert("",0,text=row[1],values=row[2:])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.date.get()) != 0 and len(self.address.get()) != 0 and len(self.service.get()) != 0 and len(self.ID_.get()) != 0 and len(self.email.get()) != 0

    def add_invoice(self):
        if self.validation():
            query = "INSERT INTO invoices VALUES(NULL,?,?,?,?,?,?,?,?,?)"
            service_text = self.service.get()
            service_textCopy = service_text.replace(" - ₡","")
            #print(service_text)

            price = ""
            service = ""

            for i in service_textCopy:
                if not i.isalpha():
                    price += i
                else:
                    service += i

            print(self.ID_.get())
            #parameters = (self.name.get(),self.date.get(),self.date.get_date()+timedelta(days=3),self.email.get(),self.address.get(),service,float(price),self.discount.get(),self.ID_.get())
            parameters = (self.name.get(),self.ID_.get(),self.email.get(),self.date.get(),self.date.get_date()+timedelta(days=3),service,float(price),self.discount.get(),self.address.get())
            self.run_query(query,parameters)
            self.message['text'] = "{}'s invoice added succesfully".format(self.name.get())
            self.message['fg'] = "green"
            self.get_single_data(self.name.get())
            self.name.delete(0,END)
            self.address.delete(0,END)
            self.ID_.delete(0,END)
            self.email.delete(0,END)
            self.service.delete(0,END)
            self.discount.delete(0,END)
        else:
            self.message['text'] = "All spaces must be filled"
            self.message['fg'] = "red"
        self.get_invoices()

    def delete_invoice(self):
        self.message['text'] = ""
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = "Please select a record"
            return
        self.message['text'] = ""
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM invoices WHERE name = ?'
        self.run_query(query,(name,))
        self.message['text'] = "Invoice deleted successfully"
        self.message['fg'] = "blue"
        self.get_invoices()

    def get_single_data(self,invoiceName):
        list = []
        # getting data
        query = 'SELECT * FROM invoices ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            print(row[1])
            if row[1] == invoiceName:
                print(row)
                invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress = row
        newInvoice = Invoice(invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress)
        newInvoice.generateInvoice()
        newInvoice.moveInvoices()



if __name__ == '__main__':
    window = Tk()
    application = InvoicesInterface(window)
    window.mainloop()
