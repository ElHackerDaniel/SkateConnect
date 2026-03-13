# config/db_config.py (versión mejorada)
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Retorna una conexión a MySQL o None si falla.
    Centraliza los parámetros y mejora el manejo de errores.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",              # cámbiala según tu MySQL
            database="reservas_skate",
            charset="utf8mb4",
            use_unicode=True,
            autocommit=False,
            raise_on_warnings=True
        )

        if connection.is_connected():
            return connection

        return None

    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

