import tkinter as tk
from PIL import Image, ImageTk
import os
import agregar_producto  # Importa el archivo para agregar productos
import mostrar_inventario  # Importa el archivo para mostrar el inventario
import descargar_reporte  # Importa el archivo de descargar reporte

# Ventana principal
root = tk.Tk()
root.title("Menú Principal - Ferretería RUPHA")
root.geometry("800x800")
root.state("zoomed")  # Maximiza la ventana

# Frame del menú principal
frame_menu = tk.Frame(root, bg="white")  # Fondo blanco opcional para el frame principal
frame_menu.pack(fill="both", expand=True)

# Ruta al archivo .ico
ruta_icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icono_empresa.ico')
if os.path.exists(ruta_icono):
    root.iconbitmap(ruta_icono)
else:
    print("Icono .ico no encontrado en la ruta especificada.")

# Frame del inventario y de descarga de reporte
frame_mostrar_inventario = mostrar_inventario.crear_frame_mostrar_inventario(root)
frame_inventario = agregar_producto.crear_frame_inventario(root, frame_mostrar_inventario)
frame_descargar_reporte = descargar_reporte.crear_frame_reporte(root)

# Función para mostrar el frame de agregar inventario
def abrir_inventario():
    frame_menu.pack_forget()
    frame_mostrar_inventario.pack_forget()
    frame_descargar_reporte.pack_forget()
    frame_inventario.pack(fill="both", expand=True)

# Función para mostrar el frame de mostrar inventario
def abrir_mostrar_inventario():
    frame_menu.pack_forget()
    frame_inventario.pack_forget()
    frame_descargar_reporte.pack_forget()
    mostrar_inventario.actualizar_frame_inventario()  # Actualizar inventario antes de mostrar
    frame_mostrar_inventario.pack(fill="both", expand=True)

# Función para mostrar el frame de descargar reporte
def abrir_descargar_reporte():
    frame_menu.pack_forget()
    frame_inventario.pack_forget()
    frame_mostrar_inventario.pack_forget()
    frame_descargar_reporte.pack(fill="both", expand=True)

# Función para volver al menú principal
def volver_menu_principal():
    frame_inventario.pack_forget()
    frame_mostrar_inventario.pack_forget()
    frame_descargar_reporte.pack_forget()
    frame_menu.pack(fill="both", expand=True)

# Función para retroceder
def retroceder():
    volver_menu_principal()  # Vuelve al menú principal

# Función para avanzar
def avanzar():
    abrir_inventario()  # Avanza a la gestión de inventario

# Configurar los botones de flechas con caracteres
btn_retroceder = tk.Button(root, text="⬅", command=retroceder, font=("Arial", 35), borderwidth=0, bg="white")
btn_avanzar = tk.Button(root, text="➡", command=avanzar, font=("Arial", 35), borderwidth=0, bg="white")

# Posicionar los botones de flecha en la esquina superior izquierda
btn_retroceder.place(x=10, y=10)
btn_avanzar.place(x=90, y=10)

# Posicionar los botones de flecha en la esquina superior izquierda
btn_retroceder.place(x=10, y=10)
btn_avanzar.place(x=90, y=10)

# Logo
ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')
if os.path.exists(ruta_logo):
    logo_img = Image.open(ruta_logo).resize((200, 200), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_menu, image=logo)
    logo_label.pack(pady=10)
else:
    print("Logo no encontrado en la ruta especificada.")

# Título de la ventana principal
titulo = tk.Label(frame_menu, text="FERRETERIA-RUPHA", bg="white", font=("Arial", 45, "bold"))
titulo.pack(pady=10)

# Frame para contener los botones
botones_frame = tk.Frame(frame_menu, bg="white")  # Fondo blanco opcional para el contenedor
botones_frame.pack(pady=15)  # Ajusta este padding para centrar el frame de los botones en el menú

# Botón para agregar producto
btn_gestionar_inventario = tk.Button(botones_frame, text="Agregar nuevo producto", command=abrir_inventario, width=29, height=4, font=("Arial", 20, "bold"), bg="black", fg="white")
btn_gestionar_inventario.grid(row=0, column=0, padx=(0, 10))  # padding derecho para separar los botones

# Botón para mostrar inventario
btn_mostrar_inventario = tk.Button(botones_frame, text="Mostrar y Editar inventario", command=abrir_mostrar_inventario, width=29, height=4, font=("Arial", 20, "bold"), bg="orange", fg="white")
btn_mostrar_inventario.grid(row=0, column=1, padx=(10, 0))  # padding izquierdo para separar los botones

# Botón para descargar reporte de inventario
btn_descargar_reporte_menu = tk.Button(frame_menu, text="Descargar reporte de inventario", command=abrir_descargar_reporte, width=29, height=4, font=("Arial", 20, "bold"), bg="lightgreen", fg="black")
btn_descargar_reporte_menu.pack(pady=10)

# Ejecutar la ventana principal
root.mainloop()
