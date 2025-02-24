from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '¡Hola,Amigos estamos de vuelta!'


if __name__ == '__main__':
    app.run(debug=True)
@app.route('/about')
def about():
    return 'Esta es la página Acerca de'