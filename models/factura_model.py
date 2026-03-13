from config.db_config import get_db_connection

def obtener_detalle_reserva(reserva_id):
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
            u.nombre AS usuario,
            e.nombre AS espacio
        FROM reservas r
        JOIN usuarios u ON u.id = r.usuario_id
        JOIN espacios e ON e.id = r.espacio_id
        WHERE r.id = %s
    """, (reserva_id,))

    reserva = cursor.fetchone()
    db.close()

    if not reserva:
        return None

    # Asegurar que fecha sea texto (para PDF)
    if hasattr(reserva["fecha"], "strftime"):
        reserva["fecha"] = reserva["fecha"].strftime("%Y-%m-%d")

    return reserva


def obtener_facturas():
    """Devuelve todas las facturas registradas."""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            f.id, 
            f.reserva_id, 
            u.nombre AS usuario, 
            f.total, 
            f.fecha_emision
        FROM facturas f
        JOIN reservas r ON f.reserva_id = r.id
        JOIN usuarios u ON r.usuario_id = u.id
        ORDER BY f.fecha_emision DESC
    """)

    data = cursor.fetchall()
    db.close()
    return data


