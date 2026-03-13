# models/user_model.py
from config.db_config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def registrar_usuario(nombre, correo, contraseña):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
    if cursor.fetchone():
        return False, "❌ El correo ya está registrado."

    contraseña_hash = generate_password_hash(contraseña)

    cursor.execute("""
        INSERT INTO usuarios (nombre, correo, contraseña, rol)
        VALUES (%s, %s, %s, 'USUARIO')
    """, (nombre, correo, contraseña_hash))

    db.commit()
    db.close()
    return True, "✔ Usuario registrado correctamente."

def iniciar_sesion(correo, contraseña):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    usuario = cursor.fetchone()
    db.close()

    if usuario and check_password_hash(usuario["contraseña"], contraseña):
        return usuario

    return None

