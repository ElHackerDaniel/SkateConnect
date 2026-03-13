from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_reporte_pdf(reservas, ruta_salida="reportes"):
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    nombre_archivo = f"reporte_reservas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    ruta_pdf = os.path.join(ruta_salida, nombre_archivo)

    c = canvas.Canvas(ruta_pdf, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "📊 Reporte de Reservas - ReservaSkate 🛹")

    c.setFont("Helvetica", 12)
    c.drawString(50, 725, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 710, f"Total de registros: {len(reservas)}")

    # Encabezados
    def draw_headers(y_pos):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y_pos, "ID")
        c.drawString(90, y_pos, "Usuario")
        c.drawString(200, y_pos, "Espacio")
        c.drawString(270, y_pos, "Fecha")
        c.drawString(350, y_pos, "Inicio")
        c.drawString(420, y_pos, "Fin")
        return y_pos - 20

    y = 680
    y = draw_headers(y)
    c.setFont("Helvetica", 10)

    for r in reservas:

        # 🔥 Obtener el espacio de manera segura (compatible con diferentes modelos)
        espacio = (
            r.get("espacio_id") or
            r.get("espacio") or
            r.get("nombre_espacio") or
            r.get("id_espacio") or
            "N/D"
        )

        if y < 50:  # Salto de página
            c.showPage()
            y = 750
            y = draw_headers(y)
            c.setFont("Helvetica", 10)

        c.drawString(50, y, str(r.get('id', '')))
        c.drawString(90, y, str(r.get('usuario', '')))
        c.drawString(200, y, str(espacio))
        c.drawString(270, y, str(r.get('fecha', '')))
        c.drawString(350, y, str(r.get('hora_inicio', '')))
        c.drawString(420, y, str(r.get('hora_fin', '')))
        y -= 18

    c.save()
    return ruta_pdf

