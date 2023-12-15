from catalogue.catalogue import Catalogue
from catalogue.object import Object
from view.view import View
import hashlib
import sqlite3
class User(Object):
    def __init__(self, id, username, mail, fullname):
        Object.__init__(self)
        self.id = id
        self.username = username
        self.mail = mail
        self.fullname = fullname
        self.is_admin = False
        self.view = View(username)
    
    def makeAdmin(self):
        self.is_admin = True
    
    @staticmethod
    def createUser(id:int, username:str, mail:str, fullname:str, passwd:str):
        user = User(id, username,mail,fullname)
        User.adduser(username,passwd)
        Catalogue().registerUser(user)
        return user
    def get_user_details(self):
        return f"Username: {self.username}, Name: {self.fullname}, Mail: {self.mail}"

    @staticmethod
    def login(user, password):
        with sqlite3.connect('auth.sql3') as db:
            c = db.cursor()
            query = c.execute('select username,password from auth where username=?',(user,))
            row = query.fetchone()
        if hashlib.sha256(password.encode()).hexdigest() == row[1]:
            return Catalogue().getUser(user)
        raise Exception("Invalid login, check credentials and retry")
    
    @staticmethod
    def adduser(user,password):
        encpass = hashlib.sha256(password.encode()).hexdigest()
        with sqlite3.connect('auth.sql3') as db:
            c = db.cursor()
            c.execute('insert into auth values (?,?)',(user,encpass))
    
    @staticmethod
    def createtable():
        with sqlite3.connect('auth.sql3') as db:
            c = db.cursor()
            c.execute('create table auth(username text, password text)')