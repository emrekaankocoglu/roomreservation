#from catalogue import Catalogue
from catalogue.object import Object
class User(Object):
    def __init__(self, id, username, mail, fullname, passwd):
        self.id = id
        self.username = username
        self.mail = mail
        self.fullname = fullname
        self.passwd = passwd
        self.view = None
    
    @staticmethod
    def createUser(id:int, username:str, mail:str, fullname:str, passwd:str):
        user = User(id, username,mail,fullname,passwd)
        return user
    def get_user_details(self):
        return f"Username: {self.username}, Name: {self.fullname}, Mail: {self.mail}, Password: {self.passwd}"
