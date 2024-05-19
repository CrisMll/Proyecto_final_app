import os
from dotenv import load_dotenv
from supabase import create_client, Client


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG=True
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key) 
    
config = {
    'development':DevelopmentConfig
}