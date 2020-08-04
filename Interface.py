import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
import sys
from new_user_class import NewUser
from face_recognition_class import FaceRecognition
import shutil
import os
import sys

class Window:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=400, height=400)
        self.master.title("Face Recognition App")
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame,text = "Login",width = 25,command = self.StartFaceRecognizer)
        self.button2 = tk.Button(self.frame,text = "Register",width = 25, command = self.register_window)
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
            user.show()
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
            #newPath = "PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020"+"NOMBRE"+".jpg"
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
