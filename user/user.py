#from catalogue import Catalogue
class User:
    def __init__(self, username, mail, fullname, passwd):
        self.username = username
        self.mail = mail
        self.fullname = fullname
        self.passwd = passwd

    def get_user_details(self):
        return f"Username: {self.username}, Name: {self.fullname}, Mail: {self.mail}, Password: {self.passwd}"
