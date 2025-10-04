from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from flask_login import (
    LoginManager, login_user, logout_user, login_required,
    current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
from controlador import validar_usuario, obtener_usuarios
from models.bd import obtener_conexion
from form import LoginForm, RegistrationForm

# ---------------- CONFIGURACIÓN ----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hola123'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# CSRF
csrf = CSRFProtect(app)

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'index'


# ---------------- MODELO USUARIO ----------------
class User(UserMixin):
    def __init__(self, id, nombre, correo, password_hash):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password_hash = password_hash


@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, correo, password FROM usuarios WHERE id=%s", (user_id,))
        row = cursor.fetchone()
    conexion.close()
    if row:
        return User(row[0], row[1], row[2], row[3])
    return None


# ---------------- RUTAS PRINCIPALES ----------------
@app.route('/')
def index():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correo = form.correo.data
        password = form.password.data

        usuario = validar_usuario(correo)

        if usuario and check_password_hash(usuario['password'], password):
            user_obj = User(usuario['id'], usuario['nombre'], usuario['correo'], usuario['password'])
            login_user(user_obj)
            flash(f"Bienvenido {usuario['nombre']}", "success")

            datos = obtener_usuarios()
            return render_template("panel.html", usuario=usuario['nombre'], datos=datos)
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("index"))


# ---------------- RUTA PÚBLICA DE REGISTRO ----------------
@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        carrera = form.carrera.data
        correo = form.correo.data
        password = form.password.data
        estatus = form.estatus.data

        pw_hash = generate_password_hash(password)

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios(nombre, apellido, correo, carrera, password, estatus) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, apellido, correo, carrera, pw_hash, estatus)
            )
        conexion.commit()
        conexion.close()

        flash("Usuario registrado correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("index"))

    return render_template("nuevo_usuario.html", form=form)


# ------------------ CRUD USUARIOS (interno) ------------------
@app.route('/usuarios')
@login_required
def listar_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, apellido, correo, carrera FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route('/usuarios/nuevo', methods=['GET', 'POST'])

def nuevo_usuario():
    # Esta ruta se puede usar como CRUD interno si quieres
    return redirect(url_for('register'))  # opcional: redirigir al registro público


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    conexion = obtener_conexion()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        carrera = request.form['carrera']

        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s, carrera=%s WHERE id=%s",
                (nombre, apellido, correo, carrera, id)
            )
        conexion.commit()
        conexion.close()

        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for("listar_usuarios"))

    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return render_template("editar_usuario.html", usuario=usuario)


@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conexion.commit()
    conexion.close()

    flash("Usuario eliminado correctamente", "danger")
    return redirect(url_for("listar_usuarios"))


# ------------------ INICIO APP ------------------
if __name__ == '__main__':
    app.run(port=3000, debug=True)


