from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import json
import csv

# --------------------------
# Configuración inicial
# --------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-123'  # CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/database/usuarios.db'
db = SQLAlchemy(app)


# --------------------------
# Modelo de base de datos
# --------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))


# --------------------------
# Formularios
# --------------------------
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')


# --------------------------
# Rutas
# --------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        nombre = form.nombre.data

        # Guardar en todos los formatos
        guardar_en_txt(nombre)
        guardar_en_json(nombre)
        guardar_en_csv(nombre)
        guardar_en_db(nombre)

        return render_template('resultado.html', nombre=nombre)
    return render_template('formulario.html', form=form)


# --------------------------
# Funciones de persistencia
# --------------------------
def guardar_en_txt(nombre):
    with open('static/datos/datos.txt', 'a') as f:
        f.write(f"{nombre}\n")


def guardar_en_json(nombre):
    data = {"nombre": nombre}
    with open('static/datos/datos.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')


def guardar_en_csv(nombre):
    with open('static/datos/datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre])


def guardar_en_db(nombre):
    nuevo_usuario = Usuario(nombre=nombre)
    db.session.add(nuevo_usuario)
    db.session.commit()


# --------------------------
# Ejecución
# --------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea la base de datos al iniciar
    app.run(debug=True)