# ------------ Importaciones ------------
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os

# ------------ Configuración de Flask y MySQL ------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-123'  # Para CSRF

# Configuración de MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:tu_contraseña@localhost/desarrollo_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------ Modelo de Base de Datos ------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), nullable=False, unique=True)


# ------------ Formulario WTForms ------------
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre:', validators=[DataRequired()])
    mail = StringField('Email:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')


# ------------ Funciones de Persistencia ------------
def guardar_en_txt(datos):
    with open('static/datos/datos.txt', 'a') as f:
        f.write(f"{datos}\n")


def guardar_en_json(datos):
    with open('static/datos/datos.json', 'a') as f:
        json.dump(datos, f)
        f.write('\n')


def guardar_en_csv(datos):
    with open('static/datos/datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datos['nombre'], datos['mail']])


def guardar_en_db(nombre, mail):
    usuario = Usuario(nombre=nombre, mail=mail)
    db.session.add(usuario)
    db.session.commit()


# ------------ Rutas ------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()

    if form.validate_on_submit():
        datos = {
            'nombre': form.nombre.data,
            'mail': form.mail.data
        }

        # Guardar en todos los formatos
        guardar_en_txt(f"{datos['nombre']} | {datos['mail']}")
        guardar_en_json(datos)
        guardar_en_csv(datos)
        guardar_en_db(datos['nombre'], datos['mail'])

        return render_template('resultado.html', nombre=datos['nombre'])

    return render_template('formulario.html', form=form)


# ------------ Inicialización ------------
if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('static/datos', exist_ok=True)

    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()

    app.run(debug=True)