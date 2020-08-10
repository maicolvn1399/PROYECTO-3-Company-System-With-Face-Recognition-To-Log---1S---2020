import tkinter as tk
import shutil
from tkinter import messagebox
import tkinter.filedialog
import sqlite3
from new_user_class import NewUser


class RegisterUserInterface:




    def __init__(self):
        self.new_window = tk.Toplevel()
        self.new_window.minsize(width=400, height=400)
        self.new_window.title("Register New User")
        self.label1 = tk.Label(self.new_window, text="Register New User")
        self.label1.place(x=5, y=10)
        self.labelName = tk.Label(self.new_window, text="Name")
        self.labelName.place(x=20, y=80)
        self.entryName = tk.Entry(self.new_window)
        self.entryName.place(x=100, y=80)
        self.labelAge = tk.Label(self.new_window, text="Age")
        self.labelAge.place(x=20, y=120)
        self.entryAge = tk.Entry(self.new_window)
        self.entryAge.place(x=100, y=120)
        self.labelID = tk.Label(self.new_window, text="ID")
        self.labelID.place(x=20, y=160)
        self.entryID = tk.Entry(self.new_window)
        self.entryID.place(x=100, y=160)
        self.labelEmail = tk.Label(self.new_window, text="Email")
        self.labelEmail.place(x=20, y=200)
        self.entryEmail = tk.Entry(self.new_window)
        self.entryEmail.place(x=100, y=200)
        self.labelAddress = tk.Label(self.new_window, text="Address")
        self.labelAddress.place(x=20, y=240)
        self.entryAddress = tk.Entry(self.new_window)
        self.entryAddress.place(x=100, y=240)
        self.buttonImages = tk.Button(self.new_window, text="Add Images", command=self.FileChooser)
        self.buttonImages.place(x=100, y=280)
        self.buttonAddNewUser = tk.Button(self.new_window, text="Add New User",command = self.add_user)
        self.buttonAddNewUser.place(x=100, y=340)
        self.labelImage = tk.Label(self.new_window, text="No selected image")
        self.labelImage.place(x=200, y=280)
        self.selectedImage = ".jpg"
        self.image_name = ""
        self.new_window.mainloop()

    def FileChooser(self):
        if self.entryName.get() != "" and self.entryAge.get() != "" and self.entryID.get() != "" and self.entryEmail.get() != "" and self.entryAddress.get() != "":
            path_to_image = tkinter.filedialog.askopenfilename(initialdir = "./Desktop/Faces/" ,title='Save file', filetypes=[("JPG",".jpg"),("GIF",".gif")],defaultextension=[("JPG",".jpg"),("GIF",".gif")])
            print(path_to_image)
            newPath = self.entryName.get()+".jpg"
            print(self.entryName.get()+".jpg")
            print('Copied image' )
            self.image_name = newPath.replace(" ","_")
            print(self.image_name)
            self.labelImage.config(text=newPath.replace(" ","_"))
            shutil.copy2(path_to_image,newPath.replace(" ","_"))
            self.uploadedImage = True
            self.selectedImage = newPath.replace(" ","_")
        else:
            messagebox.showerror("Error","All spaces should be filled")

    def add_user(self):

        new_user = NewUser(self.entryName.get(),self.entryAge.get(),self.entryID.get(),self.entryEmail.get(),self.entryAddress.get(),self.image_name)
        new_user.add_user()

        self.entryID.delete(0,"end")
        self.entryName.delete(0,"end")
        self.entryEmail.delete(0,"end")
        self.entryAddress.delete(0,"end")
        self.entryAge.delete(0,"end")
        self.labelImage.config(text="")



