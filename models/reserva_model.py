# models/reserva_model.py
from config.db_config import get_db_connection
from datetime import datetime, timedelta, date

# ============================================================
# Helpers internos
# ============================================================
def _parse_date(fecha_str):
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()

def _parse_time(hora_str):
    return datetime.strptime(hora_str, "%H:%M").time()

# ============================================================
# CREAR RESERVA
# ============================================================
def crear_reserva(usuario_id, espacio_id, fecha, hora_inicio, horas, participantes):
    db = None
    try:
        fecha_dt = _parse_date(fecha)
        hora_inicio_t = _parse_time(hora_inicio)
        horas_int = int(horas)
        participantes_int = int(participantes)

        # VALIDACIONES
        if horas_int < 3:
            return False, None, "⏱️ Mínimo 3 horas."
        if horas_int > 10:
            return False, None, "⏱️ Máximo 10 horas."
        if participantes_int < 1:
            return False, None, "👥 Debes registrar al menos 1 participante."
        if fecha_dt < date.today():
            return False, None, "❌ No puedes reservar una fecha pasada."

        # Calcular hora fin
        hora_inicio_dt = datetime.combine(fecha_dt, hora_inicio_t)
        hora_fin_dt = hora_inicio_dt + timedelta(hours=horas_int)
        hora_fin = hora_fin_dt.strftime("%H:%M")

        # Validar solapamiento
        if espacio_ocupado(espacio_id, fecha, hora_inicio, horas_int):
            return False, None, "🚫 El espacio ya está reservado en ese horario."

        db = get_db_connection()
        cursor = db.cursor()

        # Límite de 4 reservas por día
        if contar_reservas_por_dia(fecha) >= 4:
          return False, None, "❌ Sólo se permiten 4 reservas por día."

        cursor.execute("""
            INSERT INTO reservas (usuario_id, espacio_id, fecha, hora_inicio, hora_fin, horas_reservadas, participantes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            usuario_id, espacio_id, fecha, hora_inicio, hora_fin,
            horas_int, participantes_int
        ))

        db.commit()
        return True, cursor.lastrowid, "✔ Reserva creada correctamente."

    except Exception as e:
        return False, None, f"Error al crear reserva: {e}"

    finally:
        if db:
            db.close()
        
# ============================================================
# VERIFICAR SOLAPAMIENTO DE HORARIOS
# ============================================================
def espacio_ocupado(espacio_id, fecha, hora_inicio, horas):
    try:
        fecha_dt = _parse_date(fecha)
        hora_inicio_t = _parse_time(hora_inicio)
        horas_int = int(horas)
    except:
        return True

    hora_ini_dt = datetime.combine(date.today(), hora_inicio_t)
    hora_fin_dt = (hora_ini_dt + timedelta(hours=horas_int)).time()

    hora_ini_sql = hora_inicio_t.strftime("%H:%M")
    hora_fin_sql = hora_fin_dt.strftime("%H:%M")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 1 FROM reservas
        WHERE espacio_id = %s
          AND fecha = %s
          AND NOT (hora_fin <= %s OR hora_inicio >= %s)
        LIMIT 1
    """, (espacio_id, fecha_dt, hora_ini_sql, hora_fin_sql))

    ocupado = cursor.fetchone()
    db.close()
    return ocupado is not None

# ============================================================
# CONSULTAS PRINCIPALES DE USUARIO
# ============================================================
def obtener_reservas_usuario(usuario_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.id,
            r.fecha,
            r.hora_inicio,
            r.hora_fin,
            r.horas_reservadas,
            r.participantes,
            e.nombre AS espacio
        FROM reservas r
        LEFT JOIN espacios e ON e.id = r.espacio_id
        WHERE r.usuario_id = %s
        ORDER BY r.fecha DESC, r.hora_inicio ASC
    """, (usuario_id,))

    data = cursor.fetchall()
    db.close()
    return data

def cancelar_reserva(reserva_id, usuario_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, fecha FROM reservas
        WHERE id = %s AND usuario_id = %s
    """, (reserva_id, usuario_id))
    reserva = cursor.fetchone()

    if not reserva:
        return False, "🚫 No puedes cancelar esta reserva."

    fecha_reserva = reserva["fecha"]
    if isinstance(fecha_reserva, str):
        fecha_reserva = _parse_date(fecha_reserva)

    if fecha_reserva < date.today():
        return False, "❌ No puedes cancelar una reserva pasada."

    cursor.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
    db.commit()
    db.close()
    return True, "✔ Reserva cancelada."

def contar_reservas_por_dia(fecha):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(*) 
        FROM reservas 
        WHERE fecha = %s
    """, (fecha,))

    count = cursor.fetchone()[0]
    db.close()
    return count

# ============================================================
# CONSULTAS PARA ADMIN / DIRECTOR
# ============================================================
def obtener_todas_reservas():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, u.nombre AS usuario, e.nombre AS espacio,
               r.fecha, r.hora_inicio, r.hora_fin
        FROM reservas r
        JOIN usuarios u ON u.id = r.usuario_id
        JOIN espacios e ON e.id = r.espacio_id
        ORDER BY r.fecha DESC
    """)

    data = cursor.fetchall()
    db.close()
    return data

def obtener_reservas_por_dia():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT fecha, COUNT(*) AS total
        FROM reservas
        GROUP BY fecha
        ORDER BY fecha ASC
    """)

    data = cursor.fetchall()
    db.close()
    return data

def obtener_usuarios_mas_reservas(limit=5):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.nombre, COUNT(r.id) AS total_reservas
        FROM reservas r
        JOIN usuarios u ON r.usuario_id = u.id
        GROUP BY u.id
        ORDER BY total_reservas DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()
    db.close()
    return data

def obtener_ocupacion_por_espacio():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.nombre, COUNT(r.id) AS total
        FROM espacios e
        LEFT JOIN reservas r ON e.id = r.espacio_id
        GROUP BY e.id
        ORDER BY total DESC
    """)

    data = cursor.fetchall()
    db.close()
    return data

def obtener_resumen_diario():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(r.id) AS total_reservas,
            COALESCE(SUM(f.total), 0) AS total_ingresos
        FROM reservas r
        LEFT JOIN facturas f ON r.id = f.reserva_id
        WHERE r.fecha = %s
    """, (date.today(),))

    data = cursor.fetchone()
    db.close()
    return data

# ============================================================
# Espacios disponibles
# ============================================================
def obtener_espacios_disponibles():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre FROM espacios ORDER BY nombre ASC")
    espacios = cursor.fetchall()

    db.close()
    return espacios


