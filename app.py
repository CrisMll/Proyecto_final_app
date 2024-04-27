import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from supabase import create_client

#Models
from models.modelUser import ModelUser

#Entities
from models.entities.user import User

#Configuración inicial de la app
app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager_app=LoginManager(app)
login_manager_app.login_view = 'login'
csrf=CSRFProtect()


#?Conexion a la bbdd de supabase
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
app.secret_key = os.getenv('SECRET_KEY')

@login_manager_app.user_loader
def load_user(id_usuario):
    response = supabase.table('usuarios').select('*').eq('id', id_usuario).execute()
    user_data = response.data
    if user_data:
        user_data = user_data[0]
        user = User(id_usuario=user_data['id'], name=user_data['name'], email=user_data['email'], 
                    passwrd=user_data['passwrd'], role=user_data['id_rol'], favorite_recipes=user_data['favorite_recipes'])
        return user
    return None

###------------- RUTAS -----------------###

#? RUTA HOME Y PRINCIPALES DE RECETAS

@app.route("/")
def home():
    response = supabase.table("secciones").select("nombre_seccion, imagen_seccion, id_seccion").execute()
    secciones = response.data
    for seccion in secciones:
        print(seccion['id_seccion'])  
    response = supabase.table("recetas").select("nombre_receta").execute()
    recetas = response.data
    return render_template("index.html", secciones=secciones, recetas=recetas)

@app.route("/sections/<id>")
def get_section(id):
    response = supabase.table("secciones").select("id_seccion, nombre_seccion, imagen_seccion").eq("id_seccion", id).execute()
    seccion = response.data[0]
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta").eq("tipo_seccion_id", id).execute()
    recetas = response.data
    return render_template("sections.html", seccion=seccion, recetas=recetas)


@app.route("/recipe/<id>")
def get_recipe(id):
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, preparacion").eq("id_receta", id).execute()
    receta = response.data[0]
    return render_template("recipe.html", receta=receta)





#? RUTA DE RECETAS FAVORITAS

@app.route('/add_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def add_favorite(recipe_id):
    response = supabase.table("recetas").select("nombre_receta").eq("id_receta", recipe_id).execute()
    receta = response.data[0]
    nombre_receta = receta['nombre_receta']
    current_user.add_favorite_recipe(nombre_receta)
    flash('Receta agregada a favoritos.', 'success')
    return redirect(url_for('profile'))

@app.route('/remove_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def remove_favorite(recipe_id):
    response = supabase.table("recetas").select("nombre_receta").eq("id_receta", recipe_id).execute()
    receta = response.data[0]
    nombre_receta = receta['nombre_receta']
    current_user.remove_favorite_recipe(nombre_receta)
    flash('Receta agregada a favoritos.', 'success')
    return redirect(url_for('profile'))



#? CONTROL DE USUARIOS

@app.route('/login', methods=['GET', 'POST'])
def login():
    show_signup_link = False
    if request.method == 'POST':
        email = request.form['email']
        passwrd = request.form['passwrd']
        user = User.get_by_email(email)
        if user and check_password_hash(user.passwrd, passwrd):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Datos incorrectos. Por favor, inténtalo de nuevo.', 'error')
            show_signup_link = True  
    return render_template('auth/login.html', show_signup_link=show_signup_link)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        passwrd = request.form['passwrd']
        confirm_passwrd = request.form['confirm_passwrd']
        if passwrd != confirm_passwrd:
            flash('Las contraseñas no coinciden.', 'error')
        else:
            hashed_passwrd = generate_password_hash(passwrd)
            response = supabase.from_('usuarios').insert({'name': name, 'email': email, 'passwrd': hashed_passwrd}).execute()
            if response.get('error'):
                flash('El usuario ya existe.', 'error')
            else:
                flash('Registrado con éxito. Por favor, inicia sesión.', 'success')
                return redirect(url_for('login'))
    return render_template('auth/signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    favorite_recipes = current_user.get_favorite_recipes()
    return render_template('profile.html', favorite_recipes=favorite_recipes)


#? CONTACTO

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    return render_template('contact.html')




if __name__ == '__main__':
    #?configuracion para poder usar la configuracion para desarrollo creada con el objeto config y su diccionario
    csrf.init_app(app)
    #app.register_error_handler(404, status_404)
    app.run(debug=True)




