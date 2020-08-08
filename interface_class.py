import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
import sys
from new_user_class import NewUser
from face_recognition_class import FaceRecognition
from invoice_class import Invoice
import shutil
import random
import os
from tkinter import ttk
from tkcalendar import Calendar,DateEntry

import sys

class Window:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=400, height=400)
        self.master.title("Face Recognition App")
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame,text = "Login",width = 25,command = self.StartFaceRecognizer)
        self.button2 = tk.Button(self.frame,text = "Register",width = 25, command = self.register_window)
        self.buttonInvoice = tk.Button(self.frame,text = "Invoices",width = 25,command = self.InvoicesWindow)
        self.buttonInvoice.pack(padx=5,pady=15)
        self.button1.pack(padx=5,pady=5)
        self.button2.pack(padx=5, pady=10)
        self.frame.pack()
        self.uploadedImage = False

    def new_window(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = Window2(self.new_window)

    def register_window(self):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.minsize(width=400,height=400)
        self.new_window.title("Register New User")
        self.label1 = tk.Label(self.new_window,text = "Register New User")
        self.label1.place(x=5,y=10)
        self.labelName = tk.Label(self.new_window,text="Name")
        self.labelName.place(x=20,y=80)
        self.entryName = tk.Entry(self.new_window)
        self.entryName.place(x=100,y=80)
        self.labelAge = tk.Label(self.new_window,text = "Age")
        self.labelAge.place(x=20,y=120)
        self.entryAge = tk.Entry(self.new_window)
        self.entryAge.place(x=100,y=120)
        self.labelID = tk.Label(self.new_window,text = "ID")
        self.labelID.place(x=20,y=160)
        self.entryID = tk.Entry(self.new_window)
        self.entryID.place(x=100,y=160)
        self.labelEmail = tk.Label(self.new_window,text = "Email")
        self.labelEmail.place(x=20,y=200)
        self.entryEmail = tk.Entry(self.new_window)
        self.entryEmail.place(x=100,y=200)
        self.labelAddress = tk.Label(self.new_window,text = "Address")
        self.labelAddress.place(x=20,y=240)
        self.entryAddress = tk.Entry(self.new_window)
        self.entryAddress.place(x=100,y=240)
        self.buttonImages = tk.Button(self.new_window,text = "Add Images",command=self.FileChooser)
        self.buttonImages.place(x=100,y=280)
        self.buttonAddNewUser = tk.Button(self.new_window,text = "Add New User",command = self.SaveNewUser)
        self.buttonAddNewUser.place(x=100,y=340)
        self.labelImage = tk.Label(self.new_window,text = "No selected image")
        self.labelImage.place(x=200,y=280)
        self.selectedImage = ".jpg"

    def SaveNewUser(self):
        if self.entryName.get() != "" and self.entryAge.get() != "" and self.entryID.get() != "" and self.entryEmail.get() != "" and self.entryAddress.get() != "" and self.uploadedImage:
            self.uploadedImage = False
            self.labelImage.config(text="No selected image")
            name = self.entryName.get()
            age = self.entryAge.get()
            ID = self.entryID.get()
            email = self.entryEmail.get()
            address = self.entryAddress.get()
            print(self.selectedImage)
            image = self.selectedImage
            user = NewUser(name, age, ID, email, address, image)
            user.appendUser()
            user.writeInFile()
            user.readFile()
            #user.show()
            print("New user saved")
            self.entryName.delete(0,"end")
            self.entryAge.delete(0,"end")
            self.entryID.delete(0,"end")
            self.entryEmail.delete(0,"end")
            self.entryAddress.delete(0,"end")
            self.selectedImage = ".jpg"
            print("Reset self.selectedImage")
            print(self.selectedImage)
        else:
            messagebox.showerror("Error","You need to fill all the spaces and upload an image to register the user")

    def FileChooser(self):
        if self.entryName.get() != "" and self.entryAge.get() != "" and self.entryID.get() != "" and self.entryEmail.get() != "" and self.entryAddress.get() != "":

            path_to_image = tkinter.filedialog.askopenfilename(initialdir = "./Desktop/Faces/" ,title='Save file', filetypes=[("JPG",".jpg"),("GIF",".gif")],defaultextension=[("JPG",".jpg"),("GIF",".gif")])
            print(path_to_image)
            newPath = self.entryName.get()+".jpg"
            print(self.entryName.get()+".jpg")
            print('Copied image' )
            self.labelImage.config(text=newPath.replace(" ","_"))
            shutil.copy2(path_to_image,newPath.replace(" ","_"))
            self.uploadedImage = True
            self.selectedImage = newPath.replace(" ","_")
        else:
            messagebox.showerror("Error","All spaces should be filled")

    def StartFaceRecognizer(self):
        face_recognizer = FaceRecognition()
        face_recognizer.Recognize()

    def invoices_window(self):
        self.invoices_window = tk.Toplevel(self.master)
        self.invoices_window.minsize(width=400, height=500)
        self.invoices_window.title("Create Invoice")
        self.label2 = tk.Label(self.invoices_window, text="New Invoice")
        self.label2.place(x=5, y=10)
        self.labelName1 = tk.Label(self.invoices_window, text="Name")
        self.labelName1.place(x=20, y=80)
        self.entryName1 = tk.Entry(self.invoices_window)
        self.entryName1.place(x=100, y=80)
        self.labelAddress1 = tk.Label(self.invoices_window, text="Address")
        self.labelAddress1.place(x=20, y=120)
        self.entryAddress1 = tk.Entry(self.invoices_window)
        self.entryAddress1.place(x=100, y=120)
        self.labelID1 = tk.Label(self.invoices_window, text="ID")
        self.labelID1.place(x=20, y=160)
        self.entryID1 = tk.Entry(self.invoices_window)
        self.entryID1.place(x=100, y=160)
        self.labelEmail1 = tk.Label(self.invoices_window, text="Email")
        self.labelEmail1.place(x=20, y=200)
        self.entryEmail1 = tk.Entry(self.invoices_window)
        self.entryEmail1.place(x=100, y=200)

        self.labelDate1 = tk.Label(self.invoices_window, text="Creation date")
        self.labelDate1.place(x=20, y=240)
        self.calendar = DateEntry(self.invoices_window, width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        self.calendar.place(x=100, y=240)

        self.labelDiscount1 = tk.Label(self.invoices_window, text="Discount %")
        self.labelDiscount1.place(x=20, y=280)
        self.entryDiscount1 = tk.Entry(self.invoices_window)
        self.entryDiscount1.place(x=100, y=280)

        self.buttonCreateInvoice1 = tk.Button(self.invoices_window, text="Create Invoice",command=self.SaveInvoice)
        self.buttonCreateInvoice1.place(x=100, y=340)

    def SaveInvoice(self):
        if self.entryName1.get() != "" and self.entryAddress1.get() != "" and self.entryID1.get() != "" and self.entryEmail1.get() != "":
            invoiceName = self.entryName1.get()
            invoiceAddress = self.entryAddress1.get()
            invoiceID = self.entryID1.get()
            invoiceEmail = self.entryEmail1.get()
            invoiceDate = self.calendar.get()
            newInvoice = Invoice(invoiceName,invoiceAddress,invoiceID,invoiceEmail,invoiceDate,invoiceDate,"Jardineria")
            print(invoiceName)
            print(invoiceAddress)
            print(invoiceID)
            print(invoiceEmail)
            print(invoiceDate)
            newInvoice.generateInvoice()
            newInvoice.moveInvoices()
            self.entryName1.delete(0,"end")
            self.entryAddress1.delete(0,"end")
            self.entryID1.delete(0,"end")
            self.entryEmail1.delete(0,"end")
            self.calendar.delete(0,"end")
        else:
            messagebox.showerror("Error","All spaces must not be blank")

    def InvoicesWindow(self):
        """Con sqlite"""
        self.windowInvoices = tk.Toplevel()
        self.windowInvoices.title("Invoices Window")

        #Creating a Frame Container
        frame = ttk.LabelFrame(self.windowInvoices,text="Create an invoice")
        frame.grid(row=0,column=0,columnspan = 3,pady = 20 )

        #Name imput
        ttk.Label(frame,text="Name: ").grid(row=1,column=0)
        self.name = ttk.Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        #Address Input
        ttk.Label(frame,text= "Address: ").grid(row=2,column=0)
        self.address = ttk.Entry(frame)
        self.address.grid(row=2,column=1)

        #ID input
        ttk.Label(frame,text="ID: ").grid(row=3,column=0)
        self.ID_ = ttk.Entry(frame)
        self.ID_.grid(row=3,column=1)

        #Email input
        ttk.Label(frame,text = "Email: ").grid(row=4,column=0)
        self.email = ttk.Entry(frame)
        self.email.grid(row=4,column = 1)

        #Date input
        ttk.Label(frame,text="Date: ").grid(row=5,column=0)
        self.date = DateEntry(frame,width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        self.date.grid(row=5,column=1)

        #Service input
        #***** Change to a combobox ****
        ttk.Label(frame,text="Service").grid(row=6,column=0)
        self.service = ttk.Entry(frame)
        self.service.grid(row=6,column=1)

        #Button create invoice
        ttk.Button(frame,text="Create Invoice").grid(row = 7,columnspan = 2)

        #Table
        self.tree = ttk.Treeview(height=10,columns = 2)
        self.tree.grid(row=9, column=0, columnspan=2)



















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
