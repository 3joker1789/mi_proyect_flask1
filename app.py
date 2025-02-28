from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
    from flask_wtf import FlaskForm
    from wtforms import StringField, SubmitField
    from wtforms.validators import DataRequired


    class NameForm(FlaskForm):
        name = StringField('¿Cuál es tu nombre?', validators=[DataRequired()])
        submit = SubmitField('Enviar')
        from flask import Flask, render_template

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'supersecretkey'  # Required for CSRF protection

        @app.route('/form', methods=['GET', 'POST'])
        def form(self):
            form = NameForm()
            if form.validate_on_submit():
                name = form.name.data
                return render_template('resultado.html', name=name)
            return render_template('formulario.html', form=form)