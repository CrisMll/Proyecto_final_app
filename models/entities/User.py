from werkzeug.security import check_password_hash, generate_password_hash
from supabase import create_client, Client
from flask_login import UserMixin
from dotenv import load_dotenv
import os

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


class User(UserMixin):
    def __init__(self, id_usuario, name, email, passwrd, role, favorite_recipes=None):
        self.id_usuario = id_usuario
        self.name = name
        self.email = email
        self.passwrd = passwrd
        self.role = role
        self.favorite_recipes = favorite_recipes if favorite_recipes else []
        
    def get_id(self):
        return str(self.id_usuario)

    @classmethod    
    def get_by_id(cls, id_usuario):
        response = supabase.table('usuarios').select('*').eq('id', id_usuario).execute()
        user_data = response.data
        if user_data:
            user_data = user_data[0]
            return cls(user_data)
        return None

    @classmethod
    def get_by_email(cls, email):
        response = supabase.table('usuarios').select('*').eq('email', email).execute()
        user_data = response.data
        if user_data:
            user_data = user_data[0]
            return cls(id_usuario=user_data['id'], name=user_data['name'], email=user_data['email'], 
                    passwrd=user_data['passwrd'], role=user_data['id_rol'])
        return None    
    
    @classmethod
    def hash_password(cls, passwrd):
        return generate_password_hash(passwrd)
        
    @classmethod
    def check_password(cls, hashed_password, passwrd):
        return check_password_hash(hashed_password, passwrd)

    
    def add_favorite_recipe(self, recipe_name):
        response = supabase.table('usuarios').select('favorite_recipes').eq('id', self.id_usuario).execute()
        current_favorites = response.data[0]['favorite_recipes']
        if current_favorites is None:
            current_favorites = []
        if recipe_name not in current_favorites:
            current_favorites.append(recipe_name)
        supabase.table('usuarios').update({'favorite_recipes': current_favorites}).eq('id', self.id_usuario).execute()
        
    @classmethod        
    def remove_favorite_recipe(self, recipe_name):
        if recipe_name in self.favorite_recipes:
            self.favorite_recipes.remove(recipe_name)
            supabase.from_('usuarios').update({'favorite_recipes': self.favorite_recipes}).eq('id', self.id_usuario).execute()
        
    @classmethod
    def load_user(cls, id_usuario):
        response = supabase.table('usuarios').select('*').eq('id', id_usuario).execute()
        user_data = response.data
        if user_data:
            user_data = user_data[0]
            user = User(id_usuario=user_data['id'], name=user_data['name'], email=user_data['email'], 
                        passwrd=user_data['passwrd'], role=user_data['id_rol'], favorite_recipes=user_data['favorite_recipes'])
            return user
        return None