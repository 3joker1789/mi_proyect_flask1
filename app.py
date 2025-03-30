from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, validators

app = Flask(__name__)
app.secret_key = 'clave-secreta-ultrasegura'

# Configuración MySQL (¡AJUSTA ESTOS VALORES!)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Tu contraseña de MySQL
app.config['MYSQL_DB'] = 'desarrollo_web'

mysql = MySQL(app)


# Formulario de Producto
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', [validators.DataRequired()])
    precio = DecimalField('Precio', [validators.DataRequired()], places=2)
    stock = IntegerField('Stock', [validators.DataRequired()])


# Rutas CRUD
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                (form.nombre.data, float(form.precio.data), form.stock.data)
            )
            mysql.connection.commit()
            cursor.close()
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('crear_producto.html', form=form)


@app.route('/productos')
def listar_productos():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        return render_template('productos.html', productos=productos)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('index'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    cursor = mysql.connection.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
        producto = cursor.fetchone()
        form = ProductoForm(data={
            'nombre': producto[1],
            'precio': float(producto[2]),
            'stock': producto[3]
        })
        cursor.close()
        return render_template('editar_producto.html', form=form, id=id)

    form = ProductoForm()
    if form.validate_on_submit():
        try:
            cursor.execute(
                "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s",
                (form.nombre.data, float(form.precio.data), form.stock.data, id)
            )
            mysql.connection.commit()
            cursor.close()
            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('editar_producto', id=id))


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash('Producto eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('listar_productos'))


if __name__ == '__main__':
    app.run(debug=True)