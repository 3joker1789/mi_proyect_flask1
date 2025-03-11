from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambia esto en producción

class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message="El nombre es obligatorio")])
    email = StringField('Email', validators=[
        DataRequired(message="El email es obligatorio"),
        Email(message="Formato de email inválido")
    ])
    enviar = SubmitField('Enviar')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        # Redirige a resultado con parámetros en la URL
        return redirect(url_for('resultado',
                               nombre=form.nombre.data,
                               email=form.email.data))
    return render_template('formulario.html', form=form)

@app.route('/resultado')
def resultado():
    nombre = request.args.get('nombre')
    email = request.args.get('email')
    return render_template('resultado.html', nombre=nombre, email=email)

if __name__ == '__main__':
    app.run(debug=True)