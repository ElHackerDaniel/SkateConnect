# models/admin_model.py

from config.db_config import get_db_connection
from datetime import date, timedelta

# ---------------------------------------------
# Obtener todas las reservas (versión admin)
# ---------------------------------------------
def obtener_todas_reservas():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, u.nombre AS usuario, e.nombre AS espacio,
               r.fecha, r.hora_inicio, r.hora_fin
        FROM reservas r
        JOIN usuarios u ON r.usuario_id = u.id
        JOIN espacios e ON r.espacio_id = e.id
        ORDER BY r.fecha DESC, r.hora_inicio ASC
    """)

    data = cursor.fetchall()
    db.close()
    return data


# ---------------------------------------------
# Obtener facturas (Admin)
# ---------------------------------------------
def obtener_facturas():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT f.id, f.reserva_id, u.nombre AS usuario,
               f.total, f.fecha_emision
        FROM facturas f
        JOIN reservas r ON f.reserva_id = r.id
        JOIN usuarios u ON r.usuario_id = u.id
        ORDER BY f.fecha_emision DESC
    """)

    data = cursor.fetchall()
    db.close()
    return data


# ---------------------------------------------
# Contar reservas del día (dashboard admin)
# ---------------------------------------------
def contar_reservas_hoy():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM reservas WHERE fecha = %s", (date.today(),))
    total = cursor.fetchone()[0]

    db.close()
    return total


# ---------------------------------------------
# Reservas por día (últimos 7 días)
# ---------------------------------------------
def reservas_por_dia():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            fecha,
            COUNT(id) AS total_reservas,
            SUM(horas_reservadas) AS total_horas,
            SUM(participantes) AS total_personas
        FROM reservas
        GROUP BY fecha
        ORDER BY fecha ASC
    """)
    
    data = cursor.fetchall()
    db.close()
    return data

# ---------------------------------------------
# Espacios más reservados
# ---------------------------------------------
def espacios_mas_reservados(limit=5):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            e.nombre,
            COUNT(r.id) AS total_reservas,
            SUM(r.horas_reservadas) AS total_horas,
            SUM(r.participantes) AS total_personas
        FROM espacios e
        LEFT JOIN reservas r ON e.id = r.espacio_id
        GROUP BY e.id
        ORDER BY total_reservas DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()
    db.close()
    return data

# ---------------------------------------------
# Usuarios más activos
# ---------------------------------------------
def usuarios_mas_activos(limit=5):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            u.nombre,
            COUNT(r.id) AS reservas,
            SUM(r.participantes) AS personas_movidas
        FROM reservas r
        JOIN usuarios u ON r.usuario_id = u.id
        GROUP BY u.id
        ORDER BY reservas DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()
    db.close()
    return data

def obtener_resumen_diario():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(id) AS reservas_hoy,
            SUM(horas_reservadas) AS horas_hoy,
            SUM(participantes) AS personas_hoy
        FROM reservas
        WHERE fecha = %s
    """, (date.today(),))

    data = cursor.fetchone()
    db.close()
    return data