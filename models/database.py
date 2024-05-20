import os
from supabase import create_client
from dotenv import load_dotenv

# Conexión a la bbdd de supabase
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


def get_secciones():
    response = supabase.table("secciones").select("id_seccion, nombre_seccion, imagen_seccion").execute()
    return response.data

def get_recetas():
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, descripcion, preparacion").execute()
    return response.data