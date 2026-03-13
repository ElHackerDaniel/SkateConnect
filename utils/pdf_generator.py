# utils/pdf_generator.py

import os
from datetime import datetime
import matplotlib.pyplot as plt
from models.admin_model import reservas_por_dia, usuarios_mas_activos, espacios_mas_reservados

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# IMPORTS CORRECTOS (LIMPIOS)
from models.reserva_model import obtener_reservas_por_dia, obtener_usuarios_mas_reservas, obtener_ocupacion_por_espacio, obtener_todas_reservas, obtener_resumen_diario
from models.factura_model import obtener_facturas


# ============================================================
# FACTURA
# ============================================================
PRECIO_POR_PERSONA = 10000

def generar_factura_pdf(reserva, ruta_salida="facturas"):

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    nombre_archivo = f"factura_reserva_{reserva['id']}.pdf"
    ruta_pdf = os.path.join(ruta_salida, nombre_archivo)

    precio_por_persona = 10000
    participantes = reserva["participantes"]
    total = participantes * precio_por_persona

    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 750, "🧾 Factura de Reserva")

    # Datos del cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 710, "Datos del usuario:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 695, f"Nombre: {reserva['usuario']}")
    c.drawString(50, 680, f"Fecha de emisión: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Datos de la reserva
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 650, "Detalles de la reserva:")

    c.setFont("Helvetica", 11)
    c.drawString(50, 630, f"Espacio: {reserva['espacio']}")
    c.drawString(50, 615, f"Fecha reservada: {reserva['fecha']}")
    c.drawString(50, 600, f"Hora de inicio: {reserva['hora_inicio']}")
    c.drawString(50, 585, f"Horas reservadas: {reserva['horas_reservadas']}")
    c.drawString(50, 570, f"Participantes: {participantes}")

    # Precio
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, 540, "Resumen de pago:")
    c.setFont("Helvetica", 12)
    c.drawString(50, 520, f"Precio por persona: $ {precio_por_persona:,} COP")
    c.drawString(50, 505, f"Total a pagar: $ {total:,} COP")

    c.save()
    return ruta_pdf

# ============================================================
# INFORME ADMIN
# ============================================================
def generar_informe_pdf():
    carpeta = "facturas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = os.path.join(carpeta, f"informe_admin_{fecha_actual}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # ENCABEZADO
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(0, height - 100, width, 100, fill=True)
    logo_path = "static/img/logo.png"
    if os.path.exists(logo_path):
        c.drawImage(ImageReader(logo_path), 40, height - 90, width=80, height=80)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.black)
    c.drawString(150, height - 60, "Informe Diario - Sistema de Reservas SKATE")
    c.setFont("Helvetica", 10)
    c.drawString(150, height - 75, f"Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = height - 120

    # DATOS
    resumen = obtener_resumen_diario()
    reservas = obtener_todas_reservas()
    facturas = obtener_facturas()

    # RESUMEN
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Resumen del Día")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Total reservas: {resumen.get('total_reservas', 0) if resumen else 0}")
    y -= 15
    c.drawString(60, y, f"Ingresos totales: ${resumen.get('total_ingresos', 0) if resumen else 0:,}")
    y -= 30

    # TABLA RESERVAS
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Reservas Recientes")
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y, "ID")
    c.drawString(100, y, "Usuario")
    c.drawString(220, y, "Espacio")
    c.drawString(350, y, "Fecha")
    c.drawString(440, y, "Inicio")
    c.drawString(510, y, "Fin")
    y -= 10
    c.line(50, y, width - 50, y)
    y -= 15
    c.setFont("Helvetica", 9)
    for r in reservas[:15]:
        if y < 100:
            c.showPage()
            y = height - 100
        c.drawString(60, y, str(r["id"]))
        c.drawString(100, y, r["usuario"][:12])
        c.drawString(220, y, r["espacio"][:15])
        c.drawString(350, y, str(r["fecha"]))
        c.drawString(440, y, str(r["hora_inicio"]))
        c.drawString(510, y, str(r["hora_fin"]))
        y -= 15
    y -= 30

    # TABLA FACTURAS
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Facturas Emitidas")
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y, "ID")
    c.drawString(100, y, "Usuario")
    c.drawString(220, y, "Reserva")
    c.drawString(340, y, "Total")
    c.drawString(420, y, "Fecha")
    y -= 10
    c.line(50, y, width - 50, y)
    y -= 15
    c.setFont("Helvetica", 9)
    for f in facturas[:15]:
        if y < 100:
            c.showPage()
            y = height - 100
        c.drawString(60, y, str(f["id"]))
        c.drawString(100, y, f["usuario"][:12])
        c.drawString(220, y, str(f["reserva_id"]))
        c.drawString(340, y, f"${f['total']:,}")
        c.drawString(420, y, str(f["fecha_emision"]))
        y -= 15

    # FOOTER
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(50, 40, "Sistema ReservaSkate © 2025 — Informe Del Administrador")
    c.save()
    return pdf_path

# ============================================================
# INFORME DIRECTOR - GRÁFICOS
# ============================================================
def generar_informe_director_pdf():

    carpeta = "facturas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = os.path.join(carpeta, f"informe_director_{fecha_actual}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # ============================================================
    # ENCABEZADO
    # ============================================================
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(0, height - 100, width, 100, fill=True)

    logo_path = "static/img/logo.png"
    if os.path.exists(logo_path):
        c.drawImage(ImageReader(logo_path), 40, height - 90, width=80, height=80)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(150, height - 60, "Informe Global de Actividad — Dirección")

    c.setFont("Helvetica", 10)
    c.drawString(150, height - 75, f"Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 140

    # ============================================================
    # DATOS EXACTOS USADOS EN EL DASHBOARD
    # ============================================================
    director_data = {
        "por_dia": reservas_por_dia(),
        "usuarios": usuarios_mas_activos(),
        "espacios": espacios_mas_reservados()
    }

    # ============================================================
    # GRÁFICO 1 — RESERVAS POR DÍA
    # ============================================================
    data1 = director_data["por_dia"]
    if data1:
        fechas = [d["fecha"].strftime("%Y-%m-%d") for d in data1]
        totales = [d["total_reservas"] for d in data1]

        plt.figure(figsize=(5, 2))
        plt.plot(fechas, totales, marker="o")
        plt.title("Reservas por día")
        plt.tight_layout()

        img = os.path.join(carpeta, "chart_reservas.png")
        plt.savefig(img)
        plt.close()

        c.drawImage(img, 60, y - 150, width=480, height=120)
        y -= 180

    # ============================================================
    # GRÁFICO 2 — USUARIOS CON MÁS RESERVAS
    # ============================================================
    data2 = director_data["usuarios"]
    if data2:
        nombres = [u["nombre"] for u in data2]
        totales = [u["reservas"] for u in data2]

        plt.figure(figsize=(5, 2))
        plt.bar(nombres, totales)
        plt.title("Usuarios con más reservas")
        plt.tight_layout()

        img = os.path.join(carpeta, "chart_usuarios.png")
        plt.savefig(img)
        plt.close()

        c.drawImage(img, 60, y - 150, width=480, height=120)
        y -= 180

    # ============================================================
    # GRÁFICO 3 — OCUPACIÓN POR ESPACIO
    # ============================================================
    data3 = director_data["espacios"]
    if data3:
        nombres = [e["nombre"] for e in data3]
        valores = [e["total_reservas"] for e in data3]

        plt.figure(figsize=(5, 2))
        plt.pie(valores, labels=nombres, autopct="%1.1f%%")
        plt.title("Ocupación por espacio")
        plt.tight_layout()

        img = os.path.join(carpeta, "chart_espacios.png")
        plt.savefig(img)
        plt.close()

        c.drawImage(img, 60, y - 150, width=480, height=120)
        y -= 180

    # ============================================================
    # FOOTER
    # ============================================================
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(50, 40, "Sistema ReservaSkate © 2025 — Informe del Director")

    c.save()
    return pdf_path