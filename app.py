
import csv
import json

import mysql
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'desarrollo_web'
mysql.init_app(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Formulario con validación
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])


# Modelo SQLite
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(120))


# Modelo MySQL
class User(UserMixin):
    def __init__(self, id_usuario, nombre, email):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    cursor: object = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    usuario = cursor.fetchone()
    if usuario:
        return User(id_usuario=usuario[0], nombre=usuario[1], email=usuario[2])
    return None


# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = RegistroForm()
    if form.validate_on_submit():
        # Persistencia en TXT
        with open('datos/datos.txt', 'a') as f:
            f.write(f"{form.nombre.data},{form.email.data}\n")

        # Persistencia en JSON
        data = {'nombre': form.nombre.data, 'email': form.email.data}
        with open('datos/datos.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')

        # Persistencia en CSV
        with open('datos/datos.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([form.nombre.data, form.email.data])

        # Persistencia en SQLite
        nuevo_usuario = Usuario(nombre=form.nombre.data, email=form.email.data)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('resultado', nombre=form.nombre.data))
    return render_template('formulario.html', form=form)


# Rutas de persistencia
@app.route('/datos-txt')
def ver_txt():
    with open('datos/datos.txt', 'r') as f:
        datos = f.readlines()
    return render_template('resultado.html', datos=datos)


@app.route('/datos-json')
def ver_json():
    datos = []
    with open('datos/datos.json', 'r') as f:
        for line in f:
            datos.append(json.loads(line))
    return jsonify(datos)


# Autenticación
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (form.nombre.data, form.email.data, form.password.data))
        mysql.connection.commit()
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistroForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (form.email.data,))
        usuario = cursor.fetchone()
        if usuario and usuario[3] == form.password.data:
            user = User(id_usuario=usuario[0], nombre=usuario[1], email=usuario[2])
            login_user(user)
            return redirect(url_for('protegido'))
    return render_template('login.html', form=form)


@app.route('/protegido')
@login_required
def protegido():
    return "Página protegida"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)