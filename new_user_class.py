#Class to register a new user
import sqlite3

users = []

class NewUser:

    users_database = "newUsers.db"

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

    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.users_database) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result

    def validation(self,name, age, ID, email, address, image):
        return len(name) != 0 and len(age) != 0 and len(ID) != 0 and len(email) != 0 and len(address) != 0 and len(image) != 0

    def add_user(self):
        if self.validation(self.name, self.age, self.ID, self.email, self.address, self.images):
            query = "INSERT INTO newUsers VALUES(NULL,?,?,?,?,?,?)"
            parameters = (self.name,self.age,self.ID,self.address,self.images,self.email)
            self.run_query(query,parameters)
        self.get_users()

    def get_users(self):
        list = []
        #getting data
        query = 'SELECT * FROM newUsers ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            print(row)
            list += [row]
        return list









