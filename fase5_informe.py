"""
NOTAS PARA LA DEFENSA:
Este módulo aporta "Explicabilidad" (Explainable AI). 
Permite auditar el sistema guardando qué analizó la IA y qué decidió el Motor Experto. 
Demuestra que el sistema es transparente y profesional.
"""

from fpdf import FPDF # Librería estándar para generación de documentos PDF
import datetime       # Para estampar la fecha y asegurar que cada informe sea único

class PDF_Reporte(FPDF):
    # Heredamos de FPDF para personalizar el diseño corporativo.
    def header(self):
        # Fondo azul oscuro (Azul Corporativo: RGB 26, 35, 126)
        self.set_fill_color(26, 35, 126)
        self.rect(0, 0, 297, 30, 'F') # Dibujamos el rectángulo de cabecera
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(255, 255, 255) # Texto en blanco para contraste
        self.set_y(10)
        self.cell(0, 10, 'INFORME DE SESIÓN - ASISTENTE VIRTUAL', ln=True, align='C')
        self.ln(10)

    def footer(self):
        # Pie de página a 1.5 cm del final
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128) # Gris suave
        self.cell(0, 10, f'Página {self.page_no()} | Proyecto Modelos de IA', 0, 0, 'C')

def generar_pdf_resumen(historial):
    # Transforma la lista 'historial_sesion' de la RAM en un archivo físico[cite: 19].
    if not historial:
        print("⚠️ No hay datos para generar el PDF.")
        return

    # 'L' = Landscape (Horizontal) para que la tabla sea legible y ancha
    pdf = PDF_Reporte(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- CONFIGURACIÓN DE TABLA DINÁMICA ---
    # Los anchos suman 275mm, dejando margen en el A4
    anchos = [30, 20, 85, 40, 100]
    
    # Dibujo de Cabecera de Tabla con color gris (200, 200, 200)
    pdf.set_fill_color(200, 200, 200)
    pdf.set_font('Arial', 'B', 10)
    # ... bucle de títulos ...

    pdf.set_font('Arial', '', 9)
    for reg in historial:
        # CÁLCULO DE ALTURA VARIABLE:
        # Si el texto es largo, calculamos cuántas líneas ocupará para que la celda crezca
        lineas_entrada = pdf.get_string_width(reg['entrada']) // (anchos[2] - 2) + 1
        lineas_solucion = pdf.get_string_width(reg['solucion']) // (anchos[4] - 2) + 1
        max_lineas = max(lineas_entrada, lineas_solucion)
        
        alto_fila = max_lineas * 6 # 6mm por cada línea de texto
        if alto_fila < 12: alto_fila = 12 # Altura mínima estética

        x_ini = pdf.get_x()
        y_ini = pdf.get_y()

        # Salto de página automático si la tabla llega al final del folio
        if y_ini + alto_fila > 185:
            pdf.add_page()
            y_ini = pdf.get_y()

        # USO DE MULTI_CELL: Permite que el texto salte de línea dentro de la celda
        # Usamos set_xy para volver a la posición de la columna siguiente tras un multi_cell
        pdf.cell(anchos[0], alto_fila, str(reg['nombre']), 1, 0, 'C')
        pdf.multi_cell(anchos[2], alto_fila/lineas_entrada, reg['entrada'], 1, 'L')
        pdf.set_xy(x_ini + 30 + 20 + 85, y_ini) # Reposicionamos cursor.
        # ... resto de celdas ...

    # NOMBRE DE ARCHIVO ÚNICO: Formato AñoMesDía_HoraMinutoSegundo
    sufijo = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f"Informe_Sesion_{sufijo}.pdf"
    pdf.output(nombre_archivo)