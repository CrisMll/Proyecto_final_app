import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from supabase import create_client
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Models
from models.database import get_secciones, get_recetas
from models.modelUser import ModelUser
from forms import RegistrationForm

# Entities
from models.entities.user import User

# Configuración inicial de la app
app = Flask(__name__, template_folder='templates')
application = app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'
csrf = CSRFProtect(app)
app.permanent_session_lifetime = timedelta(minutes=15)

# Conexión a la bbdd de supabase
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
app.secret_key = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'img', 'img_recetas')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Crear el directorio de subida si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def home():
    secciones = get_secciones()
    recetas = get_recetas()
    return render_template("index.html", secciones=secciones, recetas=recetas)

@app.route("/home")
def home_in():
    secciones = get_secciones()
    recetas = get_recetas()
    return render_template("home_in.html", secciones=secciones, recetas=recetas)

@app.route("/sections/<id>")
def get_section(id):
    secciones = get_secciones()
    seccion = next((s for s in secciones if ["id_seccion"] == id), None)
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta").eq("tipo_seccion_id", id).execute()
    recetas = response.data
    return render_template("sections.html", seccion=seccion, recetas=recetas, secciones=secciones)

@app.route("/recipe/<id>")
def get_recipe(id):
    response = supabase.table("secciones").select("id_seccion, nombre_seccion").execute()
    secciones = response.data
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, descripcion, preparacion").eq("id_receta", id).execute()
    receta = response.data[0]
    response = supabase.table("ingredientes_recetas").select("*").eq("id_tipo_receta", id).execute()
    ingredientes_recetas = response.data
    
    ingredientes = []
    for ingrediente_receta in ingredientes_recetas:
        response = supabase.table("ingredientes").select("nombre_ingrediente").eq("id_ingrediente", ingrediente_receta["id_tipo_ingrediente"]).execute()
        ingrediente = response.data[0]
        response =  supabase.table("ingredientes_recetas").select("cantidad").eq("id_tipo_ingrediente", ingrediente_receta["id_tipo_ingrediente"]).execute()
        cantidad = response.data[0]['cantidad']
        ingrediente_con_cantidad = {'nombre_ingrediente': ingrediente['nombre_ingrediente'], 'cantidad': cantidad}
        ingredientes.append(ingrediente_con_cantidad)
        
    return render_template("recipe.html", receta=receta, secciones=secciones, ingredientes=ingredientes)

@app.route("/menu")
def menu():
    secciones = get_secciones()
    recetas = get_recetas()
    return render_template("menu.html", secciones=secciones, recetas=recetas)

# Control de usuarios
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    secciones = get_secciones()
    show_signup_link = False
    if request.method == 'POST':
        email = request.form['email']
        passwrd = request.form['passwrd']
        user = User.get_by_email(email)
        if user and check_password_hash(user.passwrd, passwrd):
            login_user(user)
            if current_user.role == 1:
                return redirect(url_for('admin_control'))
            elif current_user.role == 2:
                return redirect(url_for('profile'))
        else:
            flash('Datos incorrectos. Por favor, inténtalo de nuevo.', 'error')
            show_signup_link = True  
    return render_template('login/login.html', show_signup_link=show_signup_link, secciones=secciones)

#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    secciones = get_secciones()
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        passwrd = form.passwrd.data
        confirm_passwrd = form.confirm_passwrd.data

        if passwrd == confirm_passwrd:
            response = supabase.table('usuarios').select('*').eq('email', email).execute()
            user_exists = response.data
            if user_exists:
                flash('El usuario ya existe.', 'danger')
                return redirect(url_for('signup'))
            else:
                hashed_password = generate_password_hash(passwrd)
                response = supabase.from_('usuarios').insert({'name': name, 'email': email, 'passwrd': hashed_password}).execute()
                flash('Registrado con éxito. Por favor, inicia sesión.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('signup'))

    return render_template('login/signup.html', form=form, secciones=secciones)

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    file_handler = RotatingFileHandler('error_fun.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
    return render_template('500.html'), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_in'))


#manejo de cierre de sesión por inactividad
@app.before_request
def make_session_permanent():
    session.permanent = True

#mostrar perfil del usuario
@app.route('/profile')
@login_required
def profile():
    secciones = get_secciones()
    favorite_recipe_ids = current_user.get_favorite_recipes()  
    favorite_recipes = []

    if favorite_recipe_ids:
        # Creamos una lista para almacenar las recetas favoritas
        for recipe_id in favorite_recipe_ids:
            response = supabase.table('recetas').select('id_receta, nombre_receta, imagen_receta').eq('id_receta', recipe_id).execute()
            if response.data:
                favorite_recipes.append(response.data[0])  

    return render_template('login/profile.html', favorite_recipes=favorite_recipes, secciones=secciones)

# RUTA DE RECETAS FAVORITAS

# add favorita
@app.route('/add_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def add_favorite(recipe_id):
    current_user.add_favorite_recipe(recipe_id)
    flash('Receta añadida', 'added')
    return redirect(url_for('profile', message='added'))


# remove favorita
@app.route('/remove_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def remove_favorite(recipe_id):
    current_user.remove_favorite_recipe(recipe_id)
    flash('Receta eliminada', 'removed')
    return redirect(url_for('profile', message='removed'))


#? ROL ADMIN

# Vista cliente de admin en añadir receta. Recogida de info para mostrar secciones en desplegables.
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role == 1:
        secciones = get_secciones()
        response = supabase.table('ingredientes').select('id_ingrediente', 'nombre_ingrediente').execute()
        ingredientes = response.data
        return render_template('admin/admin.html', secciones=secciones, ingredientes=ingredientes)
    else:
        return redirect(url_for('home_in'))
    
# Admin backend para manejar los datos enviados al agregar receta
@app.route('/admin/new', methods=['POST'])
def admin_recipe():    
    secciones = get_secciones()
    if current_user.role == 1:
        if request.method == 'POST':
            nombre_receta = request.form['nombre_receta']
            descripcion = request.form['descripcion']
            tipo_seccion_id = request.form['tipo_seccion_id']
            preparacion = request.form['preparacion']
            ingredientes = request.form.getlist('ingredientes')
            imagen_receta = request.files['imagen_receta']
            filename = secure_filename(imagen_receta.filename)
            imagen_receta.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
            try:
                # Control de errores para insertar receta en la tabla 'recetas'
                response_receta = supabase.table('recetas').insert({
                    'nombre_receta': nombre_receta,
                    'imagen_receta': filename, #solo el nombre
                    'descripcion': descripcion,
                    'tipo_seccion_id': tipo_seccion_id,
                    'preparacion': preparacion,
                }).execute()

                response = supabase.table('recetas').select('id_receta').eq('nombre_receta', nombre_receta).execute()    
                id_receta = response.data[0]

                try:
                    # Insertamos ingredientes en la tabla 'ingredientes_recetas'
                    for ingrediente in ingredientes:
                        ingrediente = int(ingrediente)
                        response = supabase.table('ingredientes_recetas').insert({
                            'id_tipo_receta': id_receta['id_receta'],
                            'id_tipo_ingrediente': ingrediente
                        }).execute()
                        response = supabase.table('ingredientes_recetas').select('*').execute()    
                        receta = response.data
                        print(receta)

                except Exception as e:
                    print(f"Error al añadir ingredientes: {e}")
                    flash(f'Error al añadir ingredientes: {e}', 'error')
                    return redirect(url_for('error'))

                flash('¡Receta añadida con éxito!', 'success')
                return render_template('admin/admin_recipe.html', secciones=secciones)

            #? Si falla el insert    
            except Exception as e:
                print(f"Error al añadir la receta: {e}")
                flash(f'Error al añadir la receta: {e}', 'error')
                return redirect(url_for('error'))

    return render_template('admin/admin_recipe.html',secciones=secciones)


# Vista del perfil de admin
@app.route('/admin/profile')
def admin_profile():
    secciones = get_secciones()
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, preparacion").execute()
    recetas = response.data
    return render_template("admin/admin_profile.html", recetas=recetas,secciones=secciones)

# Vista control de admin principal
@app.route('/admin/control')
def admin_control():
    secciones = get_secciones()
    response = supabase.table("recetas").select("id_receta, nombre_receta, imagen_receta, ingredientes, preparacion").execute()
    recetas = response.data
    return render_template("admin/admin_control.html", recetas=recetas, secciones=secciones)



# CONTACTO
'''@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    return render_template('contact.html')'''


@app.route('/contact_form', methods=['GET', 'POST'])
def form_page():
    secciones = get_secciones()
    return render_template("contact.html", secciones=secciones)


# MANEJO DE VISTAS DE ERRORES

@app.errorhandler(404)
def not_found_error(error):
    flash('Ahora mismo no encontramos lo que buscas', 'danger')
    return render_template('error404_500.html'), 404

# Función para manejar el error 500
@app.errorhandler(500)
def internal_error(error):
    flash('Parece que el servidor no responde correctamente en estos momentos', 'danger')
    return render_template('error404_500.html'), 500

@app.route('/error_page')
def error():
    return render_template('error_page.html')



if __name__ == '__main__':
    #?configuracion para poder usar la configuracion para desarrollo creada con el objeto config y su diccionario
    csrf.init_app(app)
    app.run(debug=True)




