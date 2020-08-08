#Class to register a new user

users = []
class NewUser:

    def __init__(self,name,age,ID,email,address,images):
        self.name = name
        self.age = age
        self.ID = ID
        self.email = email
        self.address = address
        self.images = images

    def getUsers(self):
        return self.users

    def setUsers(self,users):
        self.users = users

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def getAge(self):
        return self.age

    def setAge(self,age):
        self.age = age

    def getID(self):
        return self.ID

    def setID(self,ID):
        self.ID = ID

    def getEmail(self):
        return self.email

    def setEmail(self,email):
        self.email = email

    def getAddress(self):
        return self.address

    def setAddress(self,address):
        self.address = address

    def getImages(self):
        return self.images

    def setImages(self,images):
        self.images = images

    def show(self):
        print(self.name)
        print(self.age)
        print(self.address)
        print(self.email)
        print(self.ID)
        print(self.images)
        print(users)
        print(len(users))

    def appendUser(self):
        users.append(self)

    def readFile(self):
        """This function reads the file of the users
        and return the content in a list"""
        path = "Users.txt"
        file = open(path)
        content = file.readlines()
        file.close()
        print(content)
        return content

    def writeInFile(self):
        """This function writes the new user on the file"""
        path = "Users.txt"
        file = open(path, "a")
        data = self.getName()+","+str(self.getAge())+","+self.getAddress()+","+self.getEmail()+","+self.getID()+","+self.getImages()
        file.write(data + "\n")
        file.close()


