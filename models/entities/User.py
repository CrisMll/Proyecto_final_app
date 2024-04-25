from werkzeug.security import check_password_hash, generate_password_hash
from supabase import create_client, Client
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id_usuario, email, passwrd, name='')-> None:
        self.id = id_usuario
        self.email = email
        self.passwrd = passwrd
        self.name = name
        
    @classmethod
    def hash_password(cls, passwrd):
        return generate_password_hash(passwrd)
        
    @classmethod
    def check_password(self, hashed_password, passwrd):
        return check_password_hash(hashed_password, passwrd)
    