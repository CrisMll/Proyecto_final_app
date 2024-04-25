from supabase import create_client, Client
from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self, supabase, user):
        try:
            supabase = supabase.table('usuarios').select('id, email, passwrd, name').filter('email', 'eq', user.email).execute()
            account = supabase['data']
            if account is not None and len(account) > 0:
                info = account[0]
                user=User(info['id'], info['email'], User.check_password(info['passwrd'],user.passwrd),info['name'])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, supabase, id_usuario):
        try:
            supabase = supabase.table('usuarios').select('id, email, name').filter('id', 'eq', id_usuario).execute()
            account = supabase['data']
            if account != None and len(account) > 0:
                info = account[0]
                logged_user=User(info['id'], info['email'], None, info['name'])
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
        
    @classmethod
    def check_username_exists(cls, supabase, username):
        try:
            existing_user = supabase.table('usuarios').select('email').filter('email', 'eq', username).execute()
            return existing_user['data'] is not None and len(existing_user['data']) > 0
        except Exception as ex:
            raise Exception(ex)

    