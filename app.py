from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# --------------------------
# 1. Configuración inicial
# --------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta'  # Obligatorio para CSRF


# --------------------------
# 2. Definición de formularios
# --------------------------
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')


# --------------------------
# 3. Rutas de la aplicación
# --------------------------
@app.route('/')
def home():
    return render_template('index.html')


# Ruta del formulario (debe estar después de la clase del formulario)
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()

    if form.validate_on_submit():
        # Si el formulario es válido, procesar datos
        nombre = form.nombre.data
        return render_template('resultado.html', nombre=nombre)

    return render_template('formulario.html', form=form)


# --------------------------
# 4. Ejecución de la app
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
