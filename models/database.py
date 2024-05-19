import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

    

def supabase_secciones():
    response = supabase.table("secciones").select("id_seccion, nombre_seccion, imagen_seccion").execute()
    secciones = response.data
    return secciones
    

def supabase_seccion(id):
    response = supabase.table("secciones").select("id_seccion, nombre_seccion, imagen_seccion").eq("id_seccion", id).execute()
    seccion = response.data[0]
    return seccion
        

def supabase_recetas():
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, preparacion").execute()
    recetas = response.data
    return recetas
        
    

def supabase_receta(id):
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, descripcion, preparacion").eq("id_receta", id).execute()
    receta = response.data[0]
    return receta


def supabase_ingredientes():
    response = supabase.table('ingredientes').select('id_ingrediente', 'nombre_ingrediente').execute()
    ingredientes = response.data
    return ingredientes