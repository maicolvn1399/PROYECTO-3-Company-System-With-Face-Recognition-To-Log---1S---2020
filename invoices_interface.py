from tkinter import ttk
from tkinter import *
from datetime import datetime, date, timedelta
from tkcalendar import Calendar, DateEntry
from C3ProyectServicios import Servicio
from invoice_class import Invoice
from email_class import SendEmail
from bank_class import GetBankInformation
from tkinter import messagebox
import os, shutil
import sqlite3


class InvoicesInterface:
    db_name = "invoices_database.db"

    db_services = 'database.db'

    db_invoices_search = "invoices_search.db"

    db_invoices_in_dollars = "invoices_dollars.db"

    listCombo = []

    def __init__(self, window):
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
                              foreground='white', borderwidth=2, date_pattern='YYYY-MM-DD')
        self.date.grid(row=5, column=1)

        # Service input
        # ***** Change to a combobox ****

        Label(frame, text="Service").grid(row=6, column=0)
        # n = StringVar()
        # self.service = ttk.Combobox(frame)
        # self.service["values"] = self.get_services()
        # self.service.set(self.get_services()[0])
        # self.service.grid(row=6, column=1)

        Button(frame, text="Select services", command=self.services_window).grid(row=6, column=1)

        Label(frame, text="TAX").grid(row=7, column=0)
        self.discount = Entry(frame)
        self.discount.grid(row=7, column=1)

        # Button create invoice
        Button(frame, text="Create Invoice", command=self.add_invoice).grid(row=8, columnspan=2, sticky=W + E)

        Button(frame, text="See invoices in dollars", command=self.invoices_dollars_window).grid(row=9, columnspan=2,
                                                                                                 sticky=W + E)

        # Output messages
        self.message = Label(frame, text="", fg='red')
        self.message.grid(row=10, column=0, columnspan=2, sticky=W + E)

        self.tree = ttk.Treeview(height=10, columns=("#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9"))
        self.tree.grid(row=11, column=0, columnspan=3)
        self.tree.heading("#0", text="Name", anchor=CENTER)
        self.tree.heading("#1", text="ID", anchor=CENTER)
        self.tree.heading("#2", text="Email", anchor=CENTER)
        self.tree.heading("#3", text="Date", anchor=CENTER)
        self.tree.heading("#4", text="Due Date", anchor=CENTER)
        self.tree.heading("#5", text="Service", anchor=CENTER)
        self.tree.heading("#6", text="Price (₡)", anchor=CENTER)
        self.tree.heading("#7", text="Discount", anchor=CENTER)

        # Buttons
        Button(text="DELETE", command=self.delete_invoice).grid(row=12, column=0, sticky=W + E)
        Button(text="Search invoices by date", command=self.search_invoices_interface).grid(row=12, column=1,
                                                                                            sticky=W + E)

        # Filling rows of table
        self.get_invoices()

    def search_invoices_interface(self):
        self.windowSearchByDate = Toplevel()
        self.windowSearchByDate.title("Search Invoices By Date")

        # Creating a frame container
        frame = LabelFrame(self.windowSearchByDate, text="Search Invoices By Date")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text="Select initial date").grid(row=1, column=0)
        self.initialDate = DateEntry(frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='YYYY-MM-DD')
        self.initialDate.grid(row=1, column=1)

        Label(frame, text="Select final date").grid(row=2, column=0)
        self.finalDate = DateEntry(frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='YYYY-MM-DD')
        self.finalDate.grid(row=2, column=1)

        # Button create invoice
        Button(frame, text="See Invoices", command=self.get_invoices_search).grid(row=3, columnspan=2, sticky=W + E)

        # Output messages
        self.message_search_invoices = Label(frame, text="", fg='red')
        self.message_search_invoices.grid(row=4, column=0, columnspan=2, sticky=W + E)

        self.searchtree = ttk.Treeview(self.windowSearchByDate, height=10, columns=("#0", "#1", "#2", "#3", "#4", "#5"))
        self.searchtree.grid(row=7, column=0, columnspan=3)
        self.searchtree.heading("#0", text="Invoice Number", anchor=CENTER)
        self.searchtree.heading("#1", text="Name", anchor=CENTER)
        self.searchtree.heading("#2", text="Price (₡)", anchor=CENTER)
        self.searchtree.heading("#3", text="Due Date", anchor=CENTER)
        self.searchtree.heading("#4", text="Total", anchor=CENTER)

        Button(self.windowSearchByDate, text="Show Invoice as a PDF file", command=self.get_data_to_show_pdf).grid(
            row=8, column=0, sticky=W + E)
        Button(self.windowSearchByDate, text="Send Invoice to Email", command=self.search_for_email).grid(row=8,
                                                                                                          column=1,
                                                                                                          sticky=W + E)

    def services_window(self):
        self.services_wind = Toplevel()
        self.services_wind.title("Select one or more services")
        self.services_wind.minsize(width=100, height=100)
        # Creating a Frame Container
        frame = LabelFrame(self.services_wind, text="Select services")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        self.serviceCombo = ttk.Combobox(frame)
        self.serviceCombo["values"] = self.get_services()
        self.serviceCombo.set(self.get_services()[0])
        self.serviceCombo.grid(row=6, column=1)

        # Output messages
        self.message_combobox_list = Label(frame, text="", fg='red')
        self.message_combobox_list.grid(row=7, column=0, columnspan=2, sticky=W + E)

        Button(frame, text="Add service", command=self.get_services_list).grid(row=8, column=1, sticky=W + E)

    def invoices_dollars_window(self):
        self.dollars_window = Toplevel()
        self.dollars_window.title("Invoices in dollars")

        # Creating a Frame Container
        frame = LabelFrame(self.dollars_window, text="Invoices in dollars")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Button(frame, text="See all invoices", command=self.get_invoices_in_dollars).grid(row=1, column=1)

        self.message_convert_dollars = Label(frame, text="", fg='red')
        self.message_convert_dollars.grid(row=10, column=0, columnspan=2, sticky=W + E)

        self.tree_dollars = ttk.Treeview(self.dollars_window, height=10, columns=("#0", "#1", "#2", "#3", "#4"))
        self.tree_dollars.grid(row=11, column=0, columnspan=3)
        self.tree_dollars.heading("#0", text="Name", anchor=CENTER)
        self.tree_dollars.heading("#1", text="Service", anchor=CENTER)
        self.tree_dollars.heading("#2", text="Price ($)", anchor=CENTER)
        self.tree_dollars.heading("#3", text="Total", anchor=CENTER)
        self.tree_dollars.heading("#4", text="Due Date", anchor=CENTER)

        Button(self.dollars_window, text="Convert ALL invoices to dollars",
               command=self.convert_all_invoices_to_dollars).grid(row=12, column=0, sticky=W + E)
        Button(self.dollars_window, text="Convert selected invoice to dollars",command = self.convert_single_invoice_to_dollars).grid(row=12, column=1, sticky=W + E)

    def get_services_list(self):
        comboboxContent = self.serviceCombo.get()
        servicesString = ""
        priceString = ""
        service = comboboxContent.replace(" - ₡", "")
        for i in service:
            if i.isalpha():
                servicesString += i
            else:
                priceString += i
        self.listCombo.append((servicesString, priceString))

        self.message_combobox_list['text'] = servicesString + " has been added"
        self.message_combobox_list['fg'] = "blue"

        print(self.listCombo)
        return self.listCombo

    def dates_validation(self):
        return self.initialDate.get() != "" and self.finalDate.get() != ""

    def run_query_search_invoices(self, query, parameters=()):
        with sqlite3.connect(self.db_invoices_search) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def run_query_invoices_dollars(self, query, parameters=()):
        with sqlite3.connect(self.db_invoices_in_dollars) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def run_query_to_delete_invoices(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def run_query_services(self, query, parameters=()):
        with sqlite3.connect(self.db_services) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_services(self):
        list = []
        # getting data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query_services(query)
        # filling data
        for row in db_rows:
            # print(row)
            itemNum, service, price = row
            list += [service + " - " + "₡" + str(price)]

        return list

    def get_invoices(self):
        # cleaning table everytime it runs
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # quering data
        query = 'SELECT * FROM invoices ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            # print(row)
            # print(row[2:5])
            self.tree.insert("", 0, text=row[1], values=row[2:])

    def get_invoices_in_dollars(self):
        # cleaning table each time it runs
        records = self.tree_dollars.get_children()
        for element in records:
            self.tree_dollars.delete(element)

        # quering data
        query = "SELECT * FROM invoices_dollars ORDER BY name DESC"
        db_rows = self.run_query_invoices_dollars(query)
        # filling rows of treeview
        for row in db_rows:
            self.tree_dollars.insert("", 0, text=row[1], values=row[2:6])

    def get_invoices_search(self):
        initialDate = self.initialDate.get_date()
        finalDate = self.finalDate.get_date()
        if self.dates_validation():
            # cleaning table
            records = self.searchtree.get_children()
            for element in records:
                self.searchtree.delete(element)

            # Getting data from database
            query = 'SELECT * FROM invoices_search ORDER BY name DESC'
            db_rows = self.run_query_search_invoices(query)
            # filling data
            for row in db_rows:
                # print(row)
                # format_str = '%d/%m/%Y'  # The format
                format_str = "%Y-%m-%d"
                datetime_obj = datetime.strptime(row[6], format_str)
                print(datetime_obj)
                if datetime.date(datetime_obj) >= initialDate and datetime.date(datetime_obj) <= finalDate:
                    self.message_search_invoices['text'] = ""
                    self.searchtree.insert("", 1, text=row[1], values=row[2:6])

        else:
            self.message_search_invoices['text'] = "Can't show information, please check the date entries"

    def validation(self):
        return len(self.name.get()) != 0 and len(self.date.get()) != 0 and len(self.address.get()) != 0 and len(
            self.ID_.get()) != 0 and len(self.email.get()) != 0

        # len(self.get_services_list) != 0

    def add_invoice(self):
        if self.validation():
            query = "INSERT INTO invoices VALUES(NULL,?,?,?,?,?,?,?,?,?)"
            query_dollars_database = "INSERT INTO invoices_dollars VALUES(NULL,?,?,?,?,?,?,?,?,?,?)"
            # service_text = self.service.get()
            # service_textCopy = service_text.replace(" - ₡","")
            # print(service_text)

            stringOfServices = ""
            stringOfPrices = ""
            stringPricesInDollars = ""
            totalDollars = 0

            for i in self.listCombo:
                print(i)
                service2, price2 = i
                stringOfServices += service2 + ","
                stringOfPrices += price2 + ","

            stringOfServices = stringOfServices[:-1]
            stringOfPrices = stringOfPrices[:-1]
            print("String of Services " + stringOfServices)
            print("String of Prices " + stringOfPrices)

            stringOfPricesCopy = stringOfPrices
            listToDollars = stringOfPricesCopy.split(",")
            print(listToDollars)

            for i in listToDollars:
                newExchangeRate = GetBankInformation()
                newCurrency = newExchangeRate.ColonToDollar(i)
                totalDollars += float(newCurrency)
                stringPricesInDollars += str(newCurrency) + ","

            stringPricesInDollars = stringPricesInDollars[:-1]

            print("Dollars: " + stringPricesInDollars)
            print("Total In Dollars " + str(totalDollars))

            # parameters = (self.name.get(),self.date.get(),self.date.get_date()+timedelta(days=3),self.email.get(),self.address.get(),service,float(price),self.discount.get(),self.ID_.get())
            parameters = (self.name.get(), self.ID_.get(), self.email.get(), self.date.get(),
                          self.date.get_date() + timedelta(days=3), stringOfServices, stringOfPrices,
                          self.discount.get(), self.address.get())
            parameters_dollars = (self.name.get(), stringOfServices, stringPricesInDollars, str(totalDollars),
                                  self.date.get_date() + timedelta(days=3), self.email.get(), self.ID_.get(),
                                  self.date.get(), self.discount.get(), self.address.get())
            self.run_query(query, parameters)
            self.run_query_invoices_dollars(query_dollars_database, parameters_dollars)
            nameForSearch = self.name.get()
            nameForInvoice = self.name.get()
            self.message['text'] = "{}'s invoice added succesfully".format(self.name.get())
            self.message['fg'] = "green"
            self.name.delete(0, END)
            self.address.delete(0, END)
            self.ID_.delete(0, END)
            self.email.delete(0, END)
            # self.service.delete(0,END)
            self.discount.delete(0, END)
        else:
            self.message['text'] = "All spaces must be filled"
            self.message['fg'] = "red"
        self.get_invoices()
        self.get_data_for_search_database(nameForSearch)
        self.get_single_data(nameForInvoice)

    def delete_invoice(self):
        self.message['text'] = ""
        try:
            # self.tree.item(self.tree.selection())['text'][0]
            self.tree.item(self.tree.selection())['text'][0]
            # print(self.tree.item(self.tree.selection())['text'][0])
            # print(self.tree.item(self.tree.selection())['text'])
            # print(self.tree.item(self.tree.selection())['values'][4])
        except IndexError as e:
            self.message['text'] = "Please select a record"
            return
        self.message['text'] = ""
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM invoices WHERE name = ?'
        query2 = 'DELETE FROM invoices_search WHERE name = ?'
        query3 = 'DELETE FROM invoices_dollars WHERE name = ?'
        self.get_info_to_delete_pdf(name)
        self.run_query_search_invoices(query2, (name,))
        self.run_query_invoices_dollars(query3, (name,))
        self.run_query(query, (name,))
        self.message['text'] = "Invoice deleted successfully"
        self.message['fg'] = "blue"
        self.get_invoices()

    def convert_single_invoice_to_dollars(self):
        try:
            self.tree_dollars.item(self.tree_dollars.selection())['text'][0]
        except IndexError as e:
            self.message_convert_dollars['text'] = "Please Select a Record"
            return
        self.message_convert_dollars['text'] = ""
        name = self.tree_dollars.item(self.tree_dollars.selection())['text']
        file_to_search = name+".pdf"
        self.delete_PDF(file_to_search)
        self.get_single_invoice_in_dollars(name)
        self.message_convert_dollars['text'] = name+"'s invoice has changed the currency to dollars ($)"

    def get_single_invoice_in_dollars(self,name):
        # getting data
        query = 'SELECT * FROM invoices_dollars ORDER BY name DESC'
        db_rows = self.run_query_invoices_dollars(query)
        # filling data
        for row in db_rows:
            print(row)
            if row[1] == name:
                invoiceNumber, invoiceToName, invoiceService, servicePrice, total, invoiceExpiringDate, invoiceEmail, invoiceID, invoiceDate, serviceDiscount, invoiceAddress = row
                self.generateInvoice(invoiceNumber,invoiceToName, invoiceID,invoiceEmail,invoiceDate,invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress)






    def get_info_to_delete_pdf(self, invoiceNameToDelete):
        # getting data
        query = 'SELECT * FROM invoices ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            # print(row)
            if row[1] == invoiceNameToDelete:
                print("Printing...")
                print(row[1])
                print(row)
                PDF_file_name = row[1] + " - " + str(row[0]) + ".pdf"
                print(PDF_file_name)
                self.delete_PDF(PDF_file_name)

    def delete_PDF(self, pdf_file):
        for subdir, dirs, files in os.walk(
                r'C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020\invoices'):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filename == pdf_file:
                    if filename:
                        os.remove(filepath)
                        # os.startfile(r"C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020\invoices\CRISTOPHER - 63.pdf")
                        print("PDF DELETED")
                    else:
                        messagebox.showerror("Error", "Can't delete PDF file")

    def delete_all_invoices(self):
        for subdir, dirs, files in os.walk(
                r'C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020\invoices'):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filename.endswith(".pdf"):
                    if filename:
                        os.remove(filepath)
                        print("PDF deleted ___deleting all invoices___")
                    else:
                        messagebox.showerror("Error", "Can't delete PDF file")

    def convert_all_invoices_to_dollars(self):
        self.delete_all_invoices()
        self.generate_all_invoices_in_dollars()
        self.message_convert_dollars['text'] = "ALL invoices have changed the currency to dollars ($)"

    def generate_all_invoices_in_dollars(self):
        listData = []
        # getting data
        query = 'SELECT * FROM invoices_dollars ORDER BY name DESC'
        db_rows = self.run_query_invoices_dollars(query)
        # filling data
        for row in db_rows:
            print(row)
            listData.append(row)
            print(listData)
            # row_data #= row
            invoiceNumber, invoiceToName, invoiceService, servicePrice, total, invoiceExpiringDate, invoiceEmail, invoiceID, invoiceDate, serviceDiscount, invoiceAddress = row
            # self.generateInvoice(invoiceNumber,invoiceToName, invoiceID,invoiceEmail,invoiceDate,invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress)

            # print("Generating pdf")
            # row_data = ()

        for data in listData:
            invoiceNumber, invoiceToName, invoiceService, servicePrice, total, invoiceExpiringDate, invoiceEmail, invoiceID, invoiceDate, serviceDiscount, invoiceAddress = data
            newDoc = Invoice(invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate,
                             invoiceService, servicePrice, serviceDiscount, invoiceAddress)
            newDoc.generateInvoice()

        self.move_pdfs()

    def move_pdfs(self):
        for subdir, dirs, files in os.walk(r'C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020'):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".pdf"):
                    print(filename)
                    destination = "invoices"
                    shutil.move(filepath, destination)
                    print("Invoices moved")

    def get_single_data(self, invoiceName):
        # getting data
        query = 'SELECT * FROM invoices ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            print(row[1])
            if row[1] == invoiceName:
                print(row)
                invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress = row
                self.generateInvoice(invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate,
                                     invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress)

    def generateInvoice(self, invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate,
                        invoiceService, servicePrice, serviceDiscount, invoiceAddress):
        newInvoice = Invoice(invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate,
                             invoiceService, servicePrice, serviceDiscount, invoiceAddress)
        newInvoice.generateInvoice()
        newInvoice.moveInvoices()

    def get_data_for_search_database(self, invoiceName):
        # getting data
        query = 'SELECT * FROM invoices ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            print(row[1])
            if row[1] == invoiceName:
                print(row)
                invoiceNumber, invoiceToName, invoiceID, invoiceEmail, invoiceDate, invoiceExpiringDate, invoiceService, servicePrice, serviceDiscount, invoiceAddress = row
                query2 = "INSERT INTO invoices_search VALUES(NULL,?,?,?,?,?,?,?)"
                parametersForSearchDatabase = (
                    invoiceNumber, invoiceToName, servicePrice, invoiceExpiringDate, servicePrice, invoiceDate,
                    invoiceEmail)
                self.run_query_search_invoices(query2, parametersForSearchDatabase)
                print("done")

    def get_data_to_show_pdf(self):
        self.message_search_invoices['text'] = ""
        try:
            self.searchtree.item(self.searchtree.selection())['text'][1]
        except IndexError as e:
            self.message_search_invoices['text'] = "Please select a record"
            return
        self.message_search_invoices['text'] = ""
        name = self.searchtree.item(self.searchtree.selection())['values'][0]
        numberOfInvoice = self.searchtree.item(self.searchtree.selection())['text']
        print(name, numberOfInvoice)
        pdf_file = name + " - " + str(numberOfInvoice) + ".pdf"
        self.open_pdf_file(pdf_file)

    def open_pdf_file(self, pdf_file):
        for subdir, dirs, files in os.walk(
                r'C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020\invoices'):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filename == pdf_file:
                    if filename:
                        os.startfile(filepath)
                        print("PDF OPENING...")
                    else:
                        messagebox.showerror("Error", "Can't open PDF file")

    def search_for_email(self):
        self.message_search_invoices['text'] = ""
        try:
            self.searchtree.item(self.searchtree.selection())['text'][1]
        except IndexError as e:
            self.message_search_invoices['text'] = "Please select a record"
            return
        self.message_search_invoices['text'] = ""
        name = self.searchtree.item(self.searchtree.selection())['values'][0]
        numberOfInvoice = self.searchtree.item(self.searchtree.selection())['text']
        print(self.searchtree.item(self.searchtree.selection()))
        print(name, numberOfInvoice)
        # pdf_file = name + " - " + str(numberOfInvoice) + ".pdf"
        self.get_pdf_to_email(name)

    def get_pdf_to_email(self, name):
        # Getting data from database
        query = 'SELECT * FROM invoices_search ORDER BY name DESC'
        db_rows = self.run_query_search_invoices(query)
        # filling data
        for row in db_rows:
            if row[2] == name:
                print(row)
                email = row[7]
                date = row[6]
                pdf_file = str(row[2])+ ".pdf"
                print(email)
                print(date)
                print(pdf_file)
                newEmail = SendEmail(email, "invoices/" + pdf_file, date)
                newEmail.send_email()
                messagebox.showinfo("Email Sent", "Your email has been sent to: " + email)

    def get_prices(self):
        # getting data
        query = 'SELECT * FROM invoices_search ORDER BY name DESC'
        db_rows = self.run_query_search_invoices(query)
        # filling data
        for row in db_rows:
            print(row[5])
            newPrice = GetBankInformation()
            newPrice.ColonToDollar(float(row[5]))
            print(row)


if __name__ == '__main__':
    window = Tk()
    application = InvoicesInterface(window)
    window.mainloop()
