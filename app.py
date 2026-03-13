from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file

# -------- MODELOS --------
from models.reserva_model import (
    obtener_reservas_por_dia,
    obtener_usuarios_mas_reservas,
    obtener_ocupacion_por_espacio,
    obtener_todas_reservas,
    obtener_resumen_diario,
    obtener_reservas_usuario,
    cancelar_reserva,
    crear_reserva,
    obtener_espacios_disponibles
)

from models.factura_model import obtener_detalle_reserva
from models.user_model import registrar_usuario, iniciar_sesion
from models.reserva_model import obtener_espacios_disponibles

# -------- ADMIN MODEL (AQUÍ ESTABA EL PROBLEMA) --------
from models.admin_model import (
    obtener_todas_reservas as admin_obtener_todas_reservas,
    obtener_facturas,
    reservas_por_dia,
    usuarios_mas_activos,
    espacios_mas_reservados
)

# -------- UTILIDADES --------
from utils.pdf_generator import generar_informe_pdf, generar_informe_director_pdf, generar_factura_pdf
from utils.report_generator import generar_reporte_pdf
from utils.decorators import login_required, admin_required, director_required
from config.db_config import get_db_connection


app = Flask(__name__)
app.secret_key = "Clave_Skate_Secret"

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route("/")
def index():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM espacios;")
        total_espacios = cursor.fetchone()[0]
        return render_template("index.html", total_espacios=total_espacios)
    except Exception:
        return "❌ Error al conectar con la base de datos"
    finally:
        if db:
            db.close()

# ============================================================
# REGISTRO
# ============================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        exito, mensaje = registrar_usuario(nombre, correo, contraseña)
        flash(mensaje, "success" if exito else "error")

        if exito:
            return redirect(url_for("login"))

    return render_template("register.html")

# ============================================================
# LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next")

    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        usuario = iniciar_sesion(correo, contraseña)
        if usuario:
            session["user_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]

            if next_page:
                return redirect(next_page)

            if usuario["rol"] == "ADMIN":
                return redirect(url_for("admin_dashboard"))
            if usuario["rol"] == "DIRECTOR":
                return redirect(url_for("director_dashboard"))
            return redirect(url_for("index"))

        flash("Correo o contraseña incorrectos.", "error")

    return render_template("login.html", next=next_page)

# ============================================================
# LOGOUT
# ============================================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))

# ============================================================
# DASHBOARD DIRECTOR
# ============================================================
@app.route("/director_dashboard")
@login_required
@director_required
def director_dashboard():
    return render_template(
        "director_dashboard.html",
        reservas_por_dia=obtener_reservas_por_dia(),
        usuarios_top=obtener_usuarios_mas_reservas(),
        ocupacion=obtener_ocupacion_por_espacio()
    )

# ============================================================
# INFORME DIRECTOR
# ============================================================
@app.route("/director_descargar_informe")
@login_required
@director_required
def director_descargar_informe():
    pdf_path = generar_informe_director_pdf()
    return send_file(pdf_path, as_attachment=True)

# ============================================================
# RESERVAR
# ============================================================
@app.route("/reservar", methods=["GET", "POST"])
@login_required
def reservar():
    # --- SI ES GET → MOSTRAR PÁGINA ---
    if request.method == "GET":
        fecha_actual = date.today().isoformat()
        fecha_max = (date.today() + timedelta(days=30)).isoformat()
        espacios = obtener_espacios_disponibles()

        return render_template(
            "reservar.html",
            fecha_actual=fecha_actual,
            fecha_max=fecha_max,
            espacios=espacios
        )

    # --- SI ES POST → PROCESAR RESERVA ---
    usuario_id = session["user_id"]

    fecha = request.form["fecha"]
    hora_inicio = request.form["hora_inicio"]
    horas = request.form["horas"]
    personas = request.form["personas"]
    espacio_id = request.form["espacio_id"]

    # --- Llamar a modelo ---
    ok, reserva_id, msg = crear_reserva(
        usuario_id,
        espacio_id,
        fecha,
        hora_inicio,
        horas,
        personas
    )

    flash(msg, "success" if ok else "error")

    if ok:
        return redirect(url_for("historial"))
    else:
        return redirect(url_for("reservar"))

# ============================================================
# RESERVAR (POST)
# ============================================================
@app.route("/reservar", methods=["POST"])
@login_required
def reservar_post():
    usuario_id = session["user_id"]
    fecha = request.form["fecha"]
    hora_inicio = request.form["hora_inicio"]
    horas = request.form["horas"]
    participantes = request.form["personas"]
    espacio_id = request.form["espacio_id"]

    ok, reserva_id, mensaje = crear_reserva(
        usuario_id, espacio_id, fecha, hora_inicio, horas, participantes
    )

    flash(mensaje, "success" if ok else "error")
    return redirect(url_for("historial"))

# ============================================================
# HISTORIAL
# ============================================================
@app.route("/historial")
@login_required
def historial():

    reservas = obtener_reservas_usuario(session["user_id"])
    fecha_hoy = date.today()

    return render_template(
        "historial.html",
        reservas=reservas,
        fecha_hoy=fecha_hoy
    )

# ============================================================
# CANCELAR RESERVA
# ============================================================
@app.route("/cancelar_reserva/<int:reserva_id>", methods=["POST"])
@login_required
def cancelar_reserva_route(reserva_id):
    exito, mensaje = cancelar_reserva(reserva_id, session["user_id"])
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("historial"))

# ============================================================
# FACTURA
# ============================================================
@app.route("/factura/<int:reserva_id>")
@login_required
def factura(reserva_id):
    reserva = obtener_detalle_reserva(reserva_id)
    pdf_path = generar_factura_pdf(reserva)
    return send_file(pdf_path, as_attachment=True)

@app.route("/admin_data")
@admin_required
def admin_data():
    return jsonify({
        "por_dia": reservas_por_dia(),
        "espacios": espacios_mas_reservados(),
        "usuarios": usuarios_mas_activos()
    })

# ============================================================
# DASHBOARD ADMIN
# ============================================================
@app.route("/admin_dashboard")
@login_required
@admin_required
def admin_dashboard():
    return render_template(
        "admin_dashboard.html",
        reservas=admin_obtener_todas_reservas(),
        facturas=obtener_facturas(),
        resumen=obtener_resumen_diario()
    )

# ============================================================
# INFORME ADMIN
# ============================================================
@app.route("/admin_descargar_informe")
@login_required
@admin_required
def admin_descargar_informe():
    pdf_path = generar_informe_pdf()
    return send_file(pdf_path, as_attachment=True)

# ============================================================
# DIRECTOR DATA (JSON)
# ============================================================
@app.route("/director_data")
@login_required
@director_required
def director_data():
    return jsonify({
        "por_dia": reservas_por_dia(),
        "usuarios": usuarios_mas_activos(),
        "espacios": espacios_mas_reservados()
    })

# ============================================================
# REPORTE GENERAL PDF
# ============================================================
@app.route("/reporte_pdf")
@login_required
def reporte_pdf():
    if session["rol"] not in ["ADMIN", "DIRECTOR"]:
        return redirect(url_for("index"))

    pdf_path = generar_reporte_pdf(admin_obtener_todas_reservas())
    return send_file(pdf_path, as_attachment=True)

@app.route("/api/reservas_count/<fecha>")
@login_required
def reservas_count_api(fecha):
    from models.reserva_model import contar_reservas_por_dia
    count = contar_reservas_por_dia(fecha)
    return {"count": count}

# ============================================================
# RUN SERVER
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)


