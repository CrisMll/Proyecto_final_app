from flask import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, email, passwrd, is_admin=False):
        self.id= id
        self.username= username
        self.email = email
        self.passwrd = generate_password_hash(passwrd)
        self.is_admin = is_admin
        
    def set_passwrd(self.passwrd):
        self.passwrd = generate_password_hash(passwrd)
        
    def check_password(self.passwrd):
        return check_password_hash(self.passwrd, passwrd)
    
    def __repr__(self):
        return '<User>'.format(self.email)