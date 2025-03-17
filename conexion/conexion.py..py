def conectar():
    try:
        import mysql.connector
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='tu_contraseña',  # Cambia por tu contraseña
            database='desarrollo_web'
        )
        return conexion
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None