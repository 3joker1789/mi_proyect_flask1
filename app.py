# ------------ Importaciones ------------
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os
from dotenv import load_dotenv  # Para variables de entorno

# Cargar variables de entorno
load_dotenv()

# ------------ Configuración de Flask y MySQL ------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')  # Clave desde .env

# Configuración corregida de MySQL (usa tu nombre de BD real)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------ Modelo de Base de Datos (Versión Mejorada) ------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), nullable=False, unique=True, index=True)  # Índice para búsquedas


# ------------ Formulario WTForms (Con Validación de Email) ------------
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre:', validators=[DataRequired(message="Campo obligatorio")])
    mail = StringField('Email:', validators=[
        DataRequired(message="Campo obligatorio"),
        Email(message="Formato de email inválido")
    ])
    enviar = SubmitField('Enviar')


# ------------ Funciones de Persistencia (Con Manejo de Errores) ------------
def guardar_en_archivo(datos, formato):
    try:
        base_path = 'static/datos'
        os.makedirs(base_path, exist_ok=True)

        if formato == 'txt':
            with open(f'{base_path}/datos.txt', 'a', encoding='utf-8') as f:
                f.write(f"{datos['nombre']} | {datos['mail']}\n")

        elif formato == 'json':
            with open(f'{base_path}/datos.json', 'a', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False)
                f.write('\n')

        elif formato == 'csv':
            file_exists = os.path.isfile(f'{base_path}/datos.csv')
            with open(f'{base_path}/datos.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Nombre', 'Email'])
                writer.writerow([datos['nombre'], datos['mail']])

        return True
    except Exception as e:
        print(f"Error al guardar en {formato}: {str(e)}")
        return False


def guardar_en_db(nombre, mail):
    try:
        if not Usuario.query.filter_by(mail=mail).first():
            usuario = Usuario(nombre=nombre, mail=mail)
            db.session.add(usuario)
            db.session.commit()
            return True
        return False  # Email ya existe
    except Exception as e:
        db.session.rollback()
        print(f"Error en DB: {str(e)}")
        return False


# ------------ Rutas Mejoradas ------------
@app.route('/')
def home():
    return render_template('index.html', usuarios=Usuario.query.limit(5).all())


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()

    if form.validate_on_submit():
        datos = {
            'nombre': form.nombre.data.strip(),
            'mail': form.mail.data.lower().strip()
        }

        # Guardar en todos los formatos
        resultados = {
            'txt': guardar_en_archivo(datos, 'txt'),
            'json': guardar_en_archivo(datos, 'json'),
            'csv': guardar_en_archivo(datos, 'csv'),
            'db': guardar_en_db(datos['nombre'], datos['mail'])
        }

        if all(resultados.values()):
            return redirect(url_for('exito'))
        else:
            return render_template('error.html', errores=resultados)

    return render_template('formulario.html', form=form)


# ------------ Inicialización Segura ------------
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Tablas creadas exitosamente")
        except Exception as e:
            print(f"Error al crear tablas: {str(e)}")

    # Verificar/crear directorio de datos
    os.makedirs('static/datos', exist_ok=True)

    app.run(debug=True, port=5001)  # Puerto alternativo para evitar conflictos