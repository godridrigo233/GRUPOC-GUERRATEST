import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import os
import sys
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk

def crear_frame_reporte(root):
    frame_reporte = tk.Frame(root, bg="white")
    
    # Cargar y colocar el logo en la esquina superior derecha
    ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')
    if os.path.exists(ruta_logo):
        try:
            # Cargar la imagen y redimensionarla si es necesario
            logo_image = Image.open(ruta_logo)
            logo_image = logo_image.resize((95, 95), Image.LANCZOS)  # Cambia el tamaño según sea necesario
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Colocar el logo en la esquina superior derecha
            logo_label = tk.Label(frame_reporte, image=logo_photo, bg="white")
            logo_label.image = logo_photo  # Mantener referencia
            logo_label.place(relx=1.0, y=20, anchor="ne", x=-20)  # Ajusta 'y' y 'x' para desplazar hacia arriba y a la derecha
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
    else:
        print("El archivo 'logo.png' no se encontró en la ruta especificada.")

    # Título
    titulo_label = tk.Label(
        frame_reporte, 
        text="DESCARGA EL REPORTE DE TU INVENTARIO", 
        font=("Arial", 35, "bold"), 
        bg="white"
    )
    titulo_label.pack(pady=40)
    
    # Espaciador para bajar los botones
    espaciador = tk.Label(frame_reporte, bg="white")
    espaciador.pack(pady=50)  # Ajusta el valor para obtener la distancia deseada
    
    # Cargar el ícono de Excel
    ruta_icono_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'excel.png')
    if os.path.exists(ruta_icono_excel):
        try:
            icono_excel_img = Image.open(ruta_icono_excel)
            icono_excel_img = icono_excel_img.resize((80, 80), Image.LANCZOS)  # Cambia el tamaño según sea necesario
            icono_excel = ImageTk.PhotoImage(icono_excel_img)
        except Exception as e:
            print(f"Error al cargar el icono de Excel: {e}")
            icono_excel = None
    else:
        print("No se encontró el ícono de Excel.")
        icono_excel = None

    btn_descargar_excel = tk.Button(
        frame_reporte,
        text="Descargar Excel",
        image=icono_excel if icono_excel else None,
        compound="top",
        command=descargar_reporte_excel,
        font=("Arial", 20, "bold"),  # ⬆️ Texto más grande y negrita
        padx=20,     # ⬅️ espacio horizontal interno
        pady=20,     # ⬆️ espacio vertical interno
        bg="#1e7145",
        fg="white",
        bd=0,
        relief="flat",
        highlightthickness=0,
        activebackground="#155e38"
    )
    if icono_excel:
        btn_descargar_excel.image = icono_excel
    btn_descargar_excel.pack(pady=20)
    
        # Cargar el ícono de PDF
    ruta_icono_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdf.png')
    if os.path.exists(ruta_icono_pdf):
        try:
            icono_pdf_img = Image.open(ruta_icono_pdf)
            icono_pdf_img = icono_pdf_img.resize((80, 80), Image.LANCZOS)
            icono_pdf = ImageTk.PhotoImage(icono_pdf_img)
        except Exception as e:
            print(f"Error al cargar el icono de PDF: {e}")
            icono_pdf = None
    else:
        print("No se encontró el ícono de PDF.")
        icono_pdf = None

    # Botón para descargar en PDF con diseño moderno
    btn_descargar_pdf = tk.Button(
        frame_reporte, 
        text="Descargar PDF", 
        image=icono_pdf if icono_pdf else None,
        compound="top",  # Ícono encima del texto
        command=descargar_reporte_pdf, 
        font=("Arial", 20, "bold"),
        padx=20,
        pady=20,
        bg="#C62828",
        fg="black",
        bd=0,
        relief="flat",
        highlightthickness=0,
        activebackground="#AD1C1C"
    )
    if icono_pdf:
        btn_descargar_pdf.image = icono_pdf  # mantener referencia

    btn_descargar_pdf.pack(pady=20)

    # Retorna el frame creado
    return frame_reporte

# Función para obtener la ruta de la base de datos
def get_database_path():
    # Detectar si estamos en el ejecutable creado por PyInstaller
    if getattr(sys, 'frozen', False):
        # Cuando se ejecuta como un ejecutable
        base_path = sys._MEIPASS
    else:
        # Cuando se ejecuta como script normal (por ejemplo, en VS Code)
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Retorna la ruta completa a ferreteria.db
    return os.path.join(base_path, "ferreteria.db")

def descargar_reporte_excel():
    # Conexión a la base de datos usando la ruta obtenida
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener datos de la tabla 'productos'
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    
    if not productos:
        messagebox.showinfo("Sin datos", "No hay registros en la base de datos para exportar.")
        return

    df = pd.DataFrame(productos, columns=columnas)

    # Crear la carpeta "Reporte" si no existe
    ruta_carpeta_reporte = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Reporte")
    os.makedirs(ruta_carpeta_reporte, exist_ok=True)

    # Generar nombre de archivo con fecha y hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta_reporte = os.path.join(ruta_carpeta_reporte, f"Reporte_Inventario-{timestamp}.xlsx")
    
    # Guardar el DataFrame en el archivo Excel
    df.to_excel(ruta_reporte, index=False)

    # Abrir el archivo Excel y ajustar el ancho de columnas
    wb = load_workbook(ruta_reporte)
    ws = wb.active

    # Ajustar ancho de columnas
    for column in ws.columns:
        max_length = max(len(str(cell.value)) for cell in column)
        column_letter = column[0].column_letter
        ws.column_dimensions[column_letter].width = max_length + 2

    # Definir estilo de borde
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))

    # Aplicar el borde a todas las celdas con datos
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.border = thin_border

    # Guardar los cambios
    wb.save(ruta_reporte)

    messagebox.showinfo("Éxito", f"El reporte ha sido descargado exitosamente en {ruta_reporte}")


def descargar_reporte_pdf():
    # Conexión a la base de datos usando la ruta obtenida
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener datos de la tabla 'productos'
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    
    if not productos:
        messagebox.showinfo("Sin datos", "No hay registros en la base de datos para exportar.")
        return
    
    # Crear la carpeta "Reporte" si no existe
    ruta_carpeta_reporte = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Reporte")
    os.makedirs(ruta_carpeta_reporte, exist_ok=True)

    # Generar nombre de archivo con fecha y hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fecha_actual = datetime.now().strftime("%d/%m/%y")
    hora_actual = datetime.now().strftime("%H : %M : %S")
    ruta_reporte_pdf = os.path.join(ruta_carpeta_reporte, f"Reporte_Inventario-{timestamp}.pdf")
    
    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Agregar el logo en la esquina superior derecha usando Pillow
    ruta_logo = 'logo.png'  # Asegúrate de que esta ruta sea correcta
    if os.path.exists(ruta_logo):
        try:
            # Abre el logo con Pillow y guarda una copia en un formato compatible si es necesario
            logo_img = Image.open(ruta_logo)
            logo_img = logo_img.convert("RGB")  # Convierte a RGB si es necesario
            logo_img.save("temp_logo.jpg")  # Guarda una copia temporal en JPG
            
            # Agrega el logo al PDF
            pdf.image("temp_logo.jpg", x=186, y=5, w=16)  # Ajusta x, y, y el ancho (w) según sea necesario
            
            # Elimina el archivo temporal después de usarlo
            os.remove("temp_logo.jpg")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")

    # Título
    pdf.set_font("Arial", "B", 22)
    pdf.cell(0, 10, "REPORTE DE INVENTARIO - RUPHA", ln=True, align="C")
    pdf.ln(5)

    # Fecha y hora de creación
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(128, 128, 128)  # Color gris
    pdf.cell(0, 10, f"Archivo creado: Fecha: {fecha_actual}         Hora: {hora_actual}", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)  # Restablece el color a negro para el resto del contenido
    pdf.ln(10)

    # Encabezado de la tabla
    pdf.set_font("Arial", "B", 12)
    col_width = 30  # Ancho de cada columna, puedes ajustarlo según sea necesario
    table_start_x = (pdf.w - (col_width * len(columnas))) / 2  # Calcula la posición inicial de la tabla para centrarla

    # Dibujar encabezado de la tabla
    pdf.set_x(table_start_x)
    for col in columnas:
        pdf.cell(col_width, 10, col, border=1, align="C")
    pdf.ln()

    # Agregar filas de datos
    pdf.set_font("Arial", "", 10)
    for producto in productos:
        pdf.set_x(table_start_x)  # Asegura que cada fila comience en la posición centrada
        for item in producto:
            pdf.cell(col_width, 10, str(item), border=1, align="C")
        pdf.ln()

    # Guardar el archivo PDF
    try:
        pdf.output(ruta_reporte_pdf)
        messagebox.showinfo("Éxito", f"El reporte PDF ha sido descargado exitosamente en {ruta_reporte_pdf}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo PDF: {e}")